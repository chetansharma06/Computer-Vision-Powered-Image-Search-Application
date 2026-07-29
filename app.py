"""Streamlit application for searching YOLO image-detection metadata."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw
from ultralytics import YOLO

from src.image_search.core import available_classes, load_metadata, search_records


ROOT = Path(__file__).resolve().parent
DEFAULT_METADATA = ROOT / "data" / "processed" / "coco-val-2017-500" / "metadata.json"
DEFAULT_MODEL = "yolo11n.pt"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


st.set_page_config(page_title="Vision Search", page_icon="🔎", layout="wide")


def initialise_state() -> None:
    defaults = {
        "records": [],
        "searched_records": [],
        "metadata_path": str(DEFAULT_METADATA),
        "image_root": "",
        "loaded_message": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


@st.cache_resource(show_spinner="Loading YOLO model…")
def get_model(model_source: str) -> YOLO:
    """Load a YOLO model once per Streamlit server."""
    return YOLO(model_source)


def model_source(path_text: str) -> str:
    candidate = Path(path_text).expanduser()
    return str(candidate) if candidate.is_file() and candidate.stat().st_size > 0 else DEFAULT_MODEL


def run_inference(image_directory: str, model_path: str, confidence: float) -> list[dict]:
    """Run YOLO over the images in one directory and return search-ready records."""
    directory = Path(image_directory).expanduser()
    if not directory.is_dir():
        raise ValueError(f"Image directory does not exist: {directory}")
    images = sorted(path for path in directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)
    if not images:
        raise ValueError("The image directory contains no JPG, JPEG, or PNG files.")

    model = get_model(model_source(model_path))
    records = []
    for image_path in images:
        result = model.predict(str(image_path), conf=confidence, verbose=False)[0]
        detections = []
        if result.boxes is not None:
            for class_id, score, box in zip(result.boxes.cls.tolist(), result.boxes.conf.tolist(), result.boxes.xyxy.tolist()):
                detections.append(
                    {"class": result.names[int(class_id)], "confidence": float(score), "bbox": [float(value) for value in box]}
                )
        counts = Counter(item["class"] for item in detections)
        records.append(
            {
                "image_path": str(image_path),
                "detections": detections,
                "class_counts": dict(counts),
                "unique_classes": sorted(counts),
                "total_objects": len(detections),
            }
        )
    return records


def image_for_record(record: dict, image_root: str) -> Path | None:
    """Find an image locally, optionally mapping old metadata paths to a new root."""
    direct = Path(record["image_path"])
    if direct.is_file():
        return direct
    if image_root:
        mapped = Path(image_root).expanduser() / direct.name
        if mapped.is_file():
            return mapped
    return None


def display_record(
    record: dict,
    image_root: str,
    show_boxes: bool,
    highlight: bool,
    selected_classes: list[str],
    threshold: float,
) -> None:
    """Render one search result without failing when source image files are absent."""
    image_path = image_for_record(record, image_root)
    matched_classes = set(cls for cls in selected_classes if isinstance(cls, str))
    displayed_detections = [
        detection
        for detection in record["detections"]
        if detection["confidence"] >= threshold
        and (not matched_classes or detection["class"] in matched_classes)
    ]

    if image_path:
        image = Image.open(image_path).convert("RGB")
        if show_boxes:
            draw = ImageDraw.Draw(image)
            for detection in displayed_detections:
                bbox = detection.get("bbox", [])
                if len(bbox) != 4:
                    continue
                draw.rectangle(bbox, outline="#ff4fc3", width=3)
                draw.text((bbox[0] + 4, max(0, bbox[1] - 18)), detection["class"], fill="#ff4fc3")
        st.image(image, use_container_width=True)
    else:
        st.warning(f"Image file unavailable: {Path(record['image_path']).name}")
    title = Path(record["image_path"]).name
    st.markdown(f"**{title}**")
    display_classes = sorted({d["class"] for d in displayed_detections})
    if highlight:
        st.success(" · ".join(display_classes) or "No detections")
    else:
        st.caption(" · ".join(display_classes) or "No detections")
    st.caption(f"{len(displayed_detections)} detections")


initialise_state()

st.title("🔎 Computer Vision Image Search")
st.caption("Load detection metadata or run YOLO on a local image folder, then filter the results by object.")

with st.sidebar:
    st.header("Data source")
    operation = st.radio("Main options", ("Load metadata", "Process images"))
    st.session_state.image_root = st.text_input(
        "Image directory override (optional)",
        value=st.session_state.image_root,
        help="Use this when metadata contains image paths from a different computer.",
    )
    st.divider()
    st.header("Display controls")
    show_boxes = st.checkbox("Show images", value=True)
    grid_columns = st.slider("Grid columns", 1, 4, 3)
    highlight_matches = st.checkbox("Highlight detected classes", value=True)

if operation == "Load metadata":
    st.subheader("Load metadata")
    metadata_path = st.text_input("Metadata path", value=st.session_state.metadata_path)
    if st.button("Load metadata", type="primary"):
        try:
            with st.spinner("Loading metadata…"):
                records = load_metadata(metadata_path)
            st.session_state.records = records
            st.session_state.searched_records = records
            st.session_state.metadata_path = metadata_path
            st.success(f"Loaded {len(records):,} image records and {len(available_classes(records))} object classes.")
        except (OSError, ValueError) as error:
            st.error(str(error))
else:
    st.subheader("Process images with YOLO")
    first, second, third = st.columns(3)
    with first:
        image_directory = st.text_input("Image directory", value=str(ROOT / "data" / "raw"))
    with second:
        local_model_path = st.text_input("YOLO model path (optional)", value=str(ROOT / "yolo11m.pt"))
    with third:
        inference_confidence = st.slider("Inference confidence", 0.05, 0.95, 0.30, 0.05)
    st.caption("If no valid local model is supplied, the compact `yolo11n.pt` model is downloaded on first use.")
    if st.button("Start inference", type="primary"):
        try:
            with st.spinner("Running object detection…"):
                records = run_inference(image_directory, local_model_path, inference_confidence)
            st.session_state.records = records
            st.session_state.searched_records = records
            st.success(f"Processed {len(records):,} images and found {len(available_classes(records))} object classes.")
        except Exception as error:
            st.error(f"Inference could not run: {error}")

records = st.session_state.records
if not records:
    st.info("Choose **Load metadata** or **Process images** to begin.")
    st.stop()

st.divider()
st.subheader("Search UI")
classes = available_classes(records)
left, middle, right = st.columns(3)
with left:
    search_mode = st.radio("Search mode", ("OR", "AND"), horizontal=True)
with middle:
    selected_classes = st.multiselect("Classes", classes)
with right:
    threshold = st.slider("Minimum confidence", 0.0, 1.0, 0.30, 0.05)

if st.button("Search images", type="primary"):
    st.session_state.searched_records = search_records(records, selected_classes, search_mode, threshold)

matches = st.session_state.searched_records
st.subheader(f"Results ({len(matches):,})")
if not matches:
    st.info("No images match the selected filters.")
    st.stop()

for start in range(0, len(matches), grid_columns):
    columns = st.columns(grid_columns)
    for column, record in zip(columns, matches[start : start + grid_columns]):
        with column:
            display_record(
                record,
                st.session_state.image_root,
                show_boxes,
                highlight_matches,
                selected_classes,
                threshold,
            )

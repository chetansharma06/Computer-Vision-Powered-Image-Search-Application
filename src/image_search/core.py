"""Pure, testable helpers for loading and searching detection metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def _as_detection(value: Any) -> dict[str, Any] | None:
    """Validate one detection while retaining fields useful to the UI."""
    if not isinstance(value, dict) or not isinstance(value.get("class"), str):
        return None
    try:
        confidence = float(value.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    return {
        "class": value["class"].strip(),
        "confidence": max(0.0, min(1.0, confidence)),
        "bbox": value.get("bbox", []),
    }


def normalise_record(value: Any) -> dict[str, Any] | None:
    """Return a consistent metadata record, or ``None`` for invalid input."""
    if not isinstance(value, dict) or not isinstance(value.get("image_path"), str):
        return None
    detections = [item for raw in value.get("detections", []) if (item := _as_detection(raw))]
    counts = Counter(item["class"] for item in detections)
    return {
        "image_path": value["image_path"],
        "detections": detections,
        "class_counts": dict(counts),
        "unique_classes": sorted(counts),
        "total_objects": len(detections),
    }


def load_metadata(path: str | Path) -> list[dict[str, Any]]:
    """Load JSON metadata and reject malformed records with a clear error."""
    source = Path(path).expanduser()
    if not source.is_file():
        raise FileNotFoundError(f"Metadata file does not exist: {source}")
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Metadata is not valid JSON: {error.msg}") from error

    if isinstance(payload, dict):
        payload = payload.get("images", payload.get("records", []))
    if not isinstance(payload, list):
        raise ValueError("Metadata must be a JSON list of image records.")

    records = [record for raw in payload if (record := normalise_record(raw))]
    if not records:
        raise ValueError("Metadata contains no valid image records.")
    return records


def available_classes(records: list[dict[str, Any]]) -> list[str]:
    """Return all detected classes in alphabetical order."""
    return sorted({label for record in records for label in record["unique_classes"]})


def search_records(
    records: list[dict[str, Any]],
    classes: list[str],
    mode: str,
    confidence: float,
) -> list[dict[str, Any]]:
    """Filter records by selected classes and minimum detection confidence."""
    selected = set(classes)
    matches: list[dict[str, Any]] = []
    for record in records:
        detected = {item["class"] for item in record["detections"] if item["confidence"] >= confidence}
        class_match = not selected or (selected <= detected if mode == "AND" else bool(selected & detected))
        if class_match:
            matches.append(record)
    return matches

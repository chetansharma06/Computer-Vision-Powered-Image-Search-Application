# Development Guide

## Project Structure

```
YOLO_IMAGE_SEARCH/
├── app.py                    # Main Streamlit application
├── setup.py                  # Package setup configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation (you are here)
├── INSTALLATION.md           # Installation guide
├── DEVELOPMENT.md            # Development guide
├── .gitignore                # Git ignore rules
├── configs/
│   └── default.yaml          # Configuration file
├── .streamlit/
│   └── config.toml           # Streamlit theme config
├── src/
│   ├── __init__.py
│   └── image_search/
│       ├── __init__.py
│       └── core.py           # Core business logic
├── test/
│   ├── __init__.py
│   └── test_core.py          # Unit tests
└── data/
    ├── raw/                  # User input images
    └── processed/
        └── coco-val-2017-500/
            └── metadata.json # Sample data
```

## Development Setup

### 1. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 2. Run Tests

```bash
# Run all tests with verbose output
python -m unittest test.test_core -v

# Run with coverage
pip install coverage
coverage run -m unittest test.test_core
coverage report
coverage html  # Generates coverage/index.html
```

### 3. Code Linting & Formatting

```bash
# Format code with black
black app.py src/ test/

# Check code style
flake8 app.py src/ test/

# Type checking
mypy app.py src/ test/
```

## Adding New Features

### Example: Adding Bounding Box Area Filter

#### 1. Update core.py

```python
def search_records_with_area_filter(
    records: list[dict[str, Any]],
    classes: list[str],
    mode: str,
    confidence: float,
    min_area: float = 0.0,  # New parameter
    max_area: float = 1.0,  # New parameter
) -> list[dict[str, Any]]:
    """Filter records by class, confidence, and bounding box area."""
    selected = set(classes)
    matches: list[dict[str, Any]] = []
    
    for record in records:
        detected = {}
        for item in record["detections"]:
            if item["confidence"] >= confidence:
                bbox = item.get("bbox", [])
                if len(bbox) == 4:
                    # Calculate area (assuming normalized coordinates 0-1)
                    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                    if min_area <= area <= max_area:
                        detected[item["class"]] = detected.get(item["class"], 0) + 1
        
        class_match = not selected or (
            selected <= set(detected) if mode == "AND" else bool(selected & set(detected))
        )
        if class_match:
            matches.append(record)
    
    return matches
```

#### 2. Add Test

```python
# In test/test_core.py

def test_search_with_area_filter(self):
    payload = [
        {
            "image_path": "one.jpg",
            "detections": [
                {"class": "cat", "confidence": 0.9, "bbox": [0.0, 0.0, 0.5, 0.5]},  # area = 0.25
                {"class": "dog", "confidence": 0.8, "bbox": [0.5, 0.5, 1.0, 1.0]},  # area = 0.25
            ]
        }
    ]
    # ... rest of test
```

#### 3. Update UI in app.py

```python
with right:
    min_area = st.slider("Min bbox area", 0.0, 1.0, 0.0, 0.01)
    max_area = st.slider("Max bbox area", 0.0, 1.0, 1.0, 0.01)

if st.button("Search images", type="primary"):
    st.session_state.searched_records = search_records_with_area_filter(
        records, selected_classes, search_mode, threshold, min_area, max_area
    )
```

#### 4. Run Tests

```bash
python -m unittest test.test_core -v
```

#### 5. Format & Lint

```bash
black app.py src/image_search/core.py test/test_core.py
flake8 app.py src/image_search/core.py test/test_core.py
```

## Core Module Reference

### Module: src/image_search/core.py

#### Function: `load_metadata(path: str | Path) -> list[dict[str, Any]]`

**Purpose**: Load and validate JSON metadata file

**Parameters**:
- `path` (str | Path): Path to JSON metadata file

**Returns**: 
- `list[dict]`: List of normalized image records

**Raises**:
- `FileNotFoundError`: File doesn't exist
- `ValueError`: Invalid JSON or no valid records

**Example**:
```python
from src.image_search.core import load_metadata

records = load_metadata("data/processed/metadata.json")
print(f"Loaded {len(records)} records")
```

---

#### Function: `normalise_record(value: Any) -> dict[str, Any] | None`

**Purpose**: Validate and normalize a single detection record

**Parameters**:
- `value` (Any): Raw record to validate

**Returns**: 
- `dict | None`: Normalized record or None if invalid

**Internal Use**: Called by `load_metadata()`

---

#### Function: `available_classes(records: list[dict[str, Any]]) -> list[str]`

**Purpose**: Get all unique detected classes from records

**Parameters**:
- `records` (list[dict]): List of image records

**Returns**: 
- `list[str]`: Sorted list of unique class names

**Example**:
```python
from src.image_search.core import available_classes

classes = available_classes(records)
print(f"Classes: {classes}")  # ['car', 'dog', 'person', ...]
```

---

#### Function: `search_records(records, classes, mode, confidence) -> list[dict[str, Any]]`

**Purpose**: Filter records by class and confidence threshold

**Parameters**:
- `records` (list[dict]): List of image records
- `classes` (list[str]): Classes to search for
- `mode` (str): "AND" or "OR"
  - "AND": Image must contain ALL selected classes
  - "OR": Image must contain ANY selected class
- `confidence` (float): Minimum confidence threshold (0.0 - 1.0)

**Returns**: 
- `list[dict]`: Filtered list of matching records

**Example**:
```python
from src.image_search.core import search_records

# Find images with both person AND car with confidence >= 0.7
matches = search_records(records, ["person", "car"], "AND", 0.7)

# Find images with dog OR cat with confidence >= 0.5
matches = search_records(records, ["dog", "cat"], "OR", 0.5)
```

---

## Record Format

### Input Metadata Format (JSON)

```json
[
  {
    "image_path": "path/to/image.jpg",
    "detections": [
      {
        "class": "person",
        "confidence": 0.95,
        "bbox": [x1, y1, x2, y2]
      },
      {
        "class": "car",
        "confidence": 0.87,
        "bbox": [x1, y1, x2, y2]
      }
    ]
  }
]
```

### Normalized Record Format (Internal)

```python
{
    "image_path": "path/to/image.jpg",
    "detections": [
        {
            "class": "person",
            "confidence": 0.95,
            "bbox": [x1, y1, x2, y2]
        },
        {
            "class": "car",
            "confidence": 0.87,
            "bbox": [x1, y1, x2, y2]
        }
    ],
    "class_counts": {
        "person": 1,
        "car": 1
    },
    "unique_classes": ["car", "person"],
    "total_objects": 2
}
```

## YOLO Model Details

### Supported Models

| Model | Size | Speed | Accuracy | Notes |
|-------|------|-------|----------|-------|
| YOLOv11n | 2.6M | Very fast | Lower | Best for real-time |
| YOLOv11s | 6.3M | Fast | Medium | Balanced |
| YOLOv11m | 16.4M | Medium | Good | Default choice |
| YOLOv11l | 25.3M | Slower | Higher | Best accuracy |
| YOLOv11x | 56.9M | Very slow | Highest | Not recommended |

### Inference Configuration

```python
# In app.py - run_inference()
result = model.predict(
    str(image_path),
    conf=confidence,  # Confidence threshold (0-1)
    verbose=False      # Suppress output
)[0]
```

## Testing Guidelines

### Writing Tests

```python
import unittest
from src.image_search.core import search_records

class TestSearchRecords(unittest.TestCase):
    def setUp(self):
        """Runs before each test"""
        self.records = [...]
    
    def test_or_mode_returns_union(self):
        """Test OR mode returns union of selected classes"""
        result = search_records(self.records, ["cat"], "OR", 0.7)
        self.assertEqual(len(result), 2)
    
    def tearDown(self):
        """Runs after each test"""
        pass

if __name__ == "__main__":
    unittest.main()
```

### Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test class
python -m unittest test.test_core.MetadataTests

# Run specific test method
python -m unittest test.test_core.MetadataTests.test_load_and_search_metadata

# With verbose output
python -m unittest test.test_core -v

# With coverage report
coverage run -m unittest test.test_core
coverage report
```

## Code Style Guide

### Type Hints (Required)

```python
# Good
def search_records(
    records: list[dict[str, Any]],
    classes: list[str],
    mode: str,
    confidence: float,
) -> list[dict[str, Any]]:
    pass

# Bad
def search_records(records, classes, mode, confidence):
    pass
```

### Docstrings (Required for Public Functions)

```python
def load_metadata(path: str | Path) -> list[dict[str, Any]]:
    """Load JSON metadata and reject malformed records with a clear error.
    
    Args:
        path: File path to JSON metadata
        
    Returns:
        List of normalized image records
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or contains no valid records
    """
    pass
```

### Comments (Minimal)

```python
# Good - Only explains WHY, not WHAT
if isinstance(payload, dict):
    # Support both {records: [...]} and {images: [...]} formats
    payload = payload.get("images", payload.get("records", []))

# Bad - Explains obvious code
# Loop through records
for record in records:
    pass
```

### Formatting

```bash
# Use Black for auto-formatting
black app.py src/ test/

# Target line length: 88 characters (Black default)
```

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In code
logger.debug(f"Processing {len(records)} records")
```

### Use Streamlit Debug Mode

```python
# In app.py
import streamlit as st
st.set_page_config(page_title="Vision Search", page_icon="🔎")

# Add debug info
if st.sidebar.checkbox("Debug"):
    st.json({
        "Records loaded": len(st.session_state.records),
        "Search results": len(st.session_state.searched_records),
    })
```

### Profile Performance

```python
import time
import cProfile

# Simple timing
start = time.time()
# code to profile
elapsed = time.time() - start
print(f"Took {elapsed:.2f}s")

# Detailed profiling
cProfile.run('load_metadata("data/processed/metadata.json")')
```

## Deployment

### Production Checklist

- [ ] All tests pass
- [ ] Code formatted with Black
- [ ] Linting passes (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] README reviewed
- [ ] CHANGELOG updated
- [ ] Version bumped in setup.py
- [ ] Dependencies updated in requirements.txt

### Packaging

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI (if public)
pip install twine
twine upload dist/*
```

## Common Issues & Solutions

### Issue: Tests Fail with ImportError

```bash
# Solution: Ensure test/__init__.py exists
touch test/__init__.py
```

### Issue: Streamlit Won't Reload Changes

```bash
# Solution: Clear cache
streamlit cache clear

# Then restart app
streamlit run app.py
```

### Issue: YOLO Model Not Found

```bash
# Solution: Pre-download model
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [YOLO Documentation](https://docs.ultralytics.com)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)

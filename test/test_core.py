import json
import tempfile
import unittest
from pathlib import Path

from src.image_search.core import available_classes, load_metadata, search_records


class MetadataTests(unittest.TestCase):
    def test_load_and_search_metadata(self):
        payload = [
            {"image_path": "one.jpg", "detections": [{"class": "cat", "confidence": 0.9}]},
            {"image_path": "two.jpg", "detections": [{"class": "dog", "confidence": 0.8}, {"class": "cat", "confidence": 0.7}]},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metadata.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            records = load_metadata(path)

        self.assertEqual(available_classes(records), ["cat", "dog"])
        self.assertEqual([item["image_path"] for item in search_records(records, ["cat", "dog"], "AND", 0.75)], [])
        self.assertEqual([item["image_path"] for item in search_records(records, ["cat"], "OR", 0.7)], ["one.jpg", "two.jpg"])

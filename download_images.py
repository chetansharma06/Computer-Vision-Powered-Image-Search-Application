"""Download COCO images listed in metadata.json"""

import json
import os
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError
import time

# Paths
metadata_file = Path("data/processed/coco-val-2017-500/metadata.json")
output_dir = Path("data/raw/coco-val-2017-500")
output_dir.mkdir(parents=True, exist_ok=True)

# Load metadata
with open(metadata_file) as f:
    records = json.load(f)

# Extract image names from metadata
image_filenames = [Path(record["image_path"]).name for record in records]
print(f"Need to download {len(image_filenames)} images")

# COCO image URLs
base_url = "http://images.cocodataset.org/val2017/"

# Download each image
downloaded = 0
failed = 0

for i, filename in enumerate(image_filenames, 1):
    filepath = output_dir / filename
    
    # Skip if already exists
    if filepath.exists():
        print(f"[{i}/{len(image_filenames)}] OK {filename} (already exists)")
        downloaded += 1
        continue
    
    url = base_url + filename
    try:
        print(f"[{i}/{len(image_filenames)}] Downloading {filename}...", end=" ")
        urlretrieve(url, filepath)
        print("OK")
        downloaded += 1
    except URLError as e:
        print(f"FAIL - {str(e)[:50]}")
        failed += 1
        if filepath.exists():
            filepath.unlink()
    except Exception as e:
        print(f"ERROR - {str(e)[:50]}")
        failed += 1
    
    # Small delay to avoid overloading server
    if i % 10 == 0:
        time.sleep(1)

print("\n" + "="*50)
print("Download complete!")
print(f"Successfully downloaded: {downloaded}")
print(f"Failed: {failed}")
print(f"Total: {downloaded + failed}")
print(f"Images saved to: {output_dir}")

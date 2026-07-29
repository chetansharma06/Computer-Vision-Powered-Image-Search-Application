"""Resume downloading missing COCO images"""

import json
import os
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError
import time

# Paths
metadata_file = Path("data/processed/coco-val-2017-500/metadata.json")
output_dir = Path("data/raw/coco-val-2017-500")

# Load metadata
with open(metadata_file) as f:
    records = json.load(f)

# Get all needed filenames
needed_filenames = [Path(record["image_path"]).name for record in records]

# Get existing files
existing_files = set(f.name for f in output_dir.glob("*.jpg"))

# Find missing files
missing_files = [f for f in needed_filenames if f not in existing_files]

print(f"Have: {len(existing_files)}")
print(f"Need: {len(missing_files)}")
print(f"Total required: {len(needed_filenames)}")

if not missing_files:
    print("All images already downloaded!")
else:
    # COCO image URLs
    base_url = "http://images.cocodataset.org/val2017/"
    
    # Download each missing image
    downloaded = 0
    failed = 0
    
    for i, filename in enumerate(missing_files, 1):
        filepath = output_dir / filename
        url = base_url + filename
        
        try:
            print(f"[{i}/{len(missing_files)}] Downloading {filename}...", end=" ", flush=True)
            urlretrieve(url, filepath, timeout=30)
            print("OK")
            downloaded += 1
        except URLError as e:
            print(f"Failed")
            failed += 1
            if filepath.exists():
                filepath.unlink()
        except Exception as e:
            print(f"Error")
            failed += 1
        
        if i % 20 == 0:
            time.sleep(2)
    
    print(f"\nDownloaded: {downloaded}, Failed: {failed}")
    
    # Final check
    final_count = len(list(output_dir.glob("*.jpg")))
    print(f"Final total: {final_count} / {len(needed_filenames)}")

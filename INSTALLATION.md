# Installation & Setup Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: Optional but recommended for faster inference
  - NVIDIA GPU with CUDA 11.8+ for optimal performance
  - CPU mode works but is 10-30x slower

## Step-by-Step Installation

### Windows Users

#### 1. Install Python (if not already installed)
```powershell
# Download from https://www.python.org/downloads/
# Or use Windows Package Manager
winget install Python.Python.3.11
```

#### 2. Clone/Download Project
```powershell
# Extract to your desired location
# Navigate to project folder
cd YOLO_IMAGE_SEARCH
```

#### 3. Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Verify Installation
```powershell
python -m unittest test.test_core -v
```

#### 6. Run Application
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS Users

#### 1. Install Python (using Homebrew)
```bash
brew install python@3.11
```

#### 2. Setup Project
```bash
cd YOLO_IMAGE_SEARCH
```

#### 3. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Verify Installation
```bash
python -m unittest test.test_core -v
```

#### 6. Run Application
```bash
python -m streamlit run app.py
```

### Linux Users

#### 1. Install Python & Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip

# Fedora/CentOS
sudo dnf install python3.11 python3.11-devel
```

#### 2. Setup Project
```bash
cd YOLO_IMAGE_SEARCH
```

#### 3. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Verify Installation
```bash
python -m unittest test.test_core -v
```

#### 6. Run Application
```bash
python -m streamlit run app.py
```

## GPU Setup (Optional but Recommended)

### NVIDIA GPU (CUDA Support)

1. **Install CUDA Toolkit**:
   - Download from: https://developer.nvidia.com/cuda-downloads
   - Follow official NVIDIA installation guide

2. **Install cuDNN**:
   - Download from: https://developer.nvidia.com/cudnn
   - Extract and add to system PATH

3. **Install PyTorch with CUDA**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

4. **Verify GPU Detection**:
```bash
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
```

### AMD GPU (ROCm Support)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

## Docker Setup (Optional)

### Build Docker Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### Run Docker Container

```bash
# Build image
docker build -t yolo-image-search .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data yolo-image-search
```

## Troubleshooting Installation

### Issue: "No module named streamlit"
```bash
pip install streamlit
```

### Issue: "CUDA out of memory"
```python
# Reduce batch size in config or use CPU
# In app.py, use model with smaller parameters (yolo11n instead of yolo11l)
```

### Issue: "Permission denied" on Linux/macOS
```bash
chmod +x setup.py
python setup.py install
```

### Issue: Virtual environment not activating
```bash
# Windows - Use PowerShell instead of CMD
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS/Linux
source .venv/bin/activate  # Not .venv/Scripts/activate
```

## Verifying Installation

Run all checks:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list

# Run unit tests
python -m unittest test.test_core -v

# Test Streamlit
streamlit --version

# Test YOLO
python -c "from ultralytics import YOLO; print('YOLO OK')"
```

## Next Steps

1. Start the app: `streamlit run app.py`
2. Try loading sample metadata
3. Process your own images
4. Read the main README.md for usage guide

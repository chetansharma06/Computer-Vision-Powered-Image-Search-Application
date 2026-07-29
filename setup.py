"""Setup configuration for YOLO Image Search."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yolo-image-search",
    version="1.0.0",
    author="Your Organization",
    description="Interactive Streamlit app for searching YOLO object detection results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yolo-image-search",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ultralytics>=8.0.0",
        "streamlit>=1.28.0",
        "opencv-python>=4.8.0",
        "pyyaml>=6.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pillow>=10.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
)

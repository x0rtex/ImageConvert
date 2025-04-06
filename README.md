# 🖼️ Image Convert

A Python CLI tool for batch converting image files between formats with compression support and file management options.

## Features

- 🔄 Convert images between formats (via Pillow support)
- 📁 Recursive directory searching
- 🎚️ Compression/quality settings
- 🗑️ Post-conversion file management (keep/delete originals/converted files)
- 📊 Conversion statistics

## Supported Formats
Common formats include:  
`WEBP`, `JPEG`, `PNG`, `BMP`, `TIFF`, `GIF`, `ICO`, `HEIF`, `PDF` ([and more](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html))

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/x0rtex/imageconvert.git
cd image-conversion-wizard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Follow the interactive prompts:
1. 📂 Enter directory to search
2. 📤 Source file extension (e.g., jpg)
3. 📥 Target file extension (e.g., webp)
4. 🎚️ Compression/quality level (1-100)
5. 🗑️ Choose file management option after conversion

## Technical Details

**Requirements:**
- Python 3.8+ (Tested on Python 3.12)
- Pillow (PIL Fork)
- tqdm
- colorama

**Note:** Always test conversions with a copy of your files before performing bulk operations.
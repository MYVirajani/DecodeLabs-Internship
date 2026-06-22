# 📝 OCR Text Recognition 


A Streamlit web app that extracts text from images using a full pre-processing
pipeline followed by Google's Tesseract OCR engine.

---

## 📁 Project Structure
```
OCR Text Recognition/
├── app.py           ← Streamlit UI
├── ocr_engine.py    ← Pre-processing + pytesseract OCR logic
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Component       | Tool                        |
|-----------------|-----------------------------|
| UI              | Streamlit                   |
| Pre-processing  | OpenCV (cv2)                |
| OCR Engine      | pytesseract (Google Tesseract) |
| Image handling  | Pillow, NumPy               |
| Language        | Python 3.10+                |

---

## 🪟 Windows Setup

### Step 1 – Install Tesseract
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default path: `C:\Program Files\Tesseract-OCR\`
3. Open `ocr_engine.py` and uncomment this line at the top:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Step 2 – Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Run
```bash
streamlit run app.py
```
Opens at → **http://localhost:8501**

---

## 🧠 How the Pipeline Works

```
Raw Image (PNG / JPG / BMP / TIFF)
    │
    ▼
Step 1 · Grayscale Conversion
    Collapses RGB 3-channel matrix → 1D intensity matrix
    Removes distracting colour data
    │
    ▼
Step 2 · Gaussian Blur
    Smooths micro-noise and artifact imperfections
    Kernel: 3×3
    │
    ▼
Step 3 · Otsu Thresholding
    Auto-finds optimal pixel cutoff value
    Forces every pixel → pure black (0) or white (255)
    Maximises character contrast for Tesseract
    │
    ▼
Step 4 · Deskew
    Detects tilt angle via cv2.minAreaRect
    Rotates image back to horizontal baseline via warpAffine
    │
    ▼
Tesseract OCR  (--oem 3, configurable PSM)
    │
    ▼
Output: Extracted text string + confidence score (0–100%)
```

### PSM Modes
| PSM | Best for |
|-----|----------|
| 3   | General images, mixed layouts (default) |
| 6   | Books, paragraphs, uniform text blocks |
| 7   | Single line — number plates, headers |
| 11  | Invoices, scattered / sparse text |

---

## ✅ Milestone Validation

| Checkpoint | How it's met |
|---|---|
| 1. Library Integration | pytesseract integrated cleanly, error-free |
| 2. Pre-Processing Integrity | Grayscale → Blur → Otsu Threshold → Deskew (shown as 4 tabs in UI) |
| 3. Accuracy Benchmarking | Word-level mean confidence displayed; 80% gate shown as PASS/FAIL |
| 4. Visual Confirmation | Extracted text displayed in UI + downloadable .txt report |

---

## 📸 Best images to test with
- Screenshot of any document or article
- Photo of a printed sign or book page
- Scanned invoice or form
- Any image with clear, readable text

import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def to_grayscale(img_array: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

def apply_blur(gray: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(gray, (3, 3), 0)

def apply_threshold(blurred: np.ndarray) -> np.ndarray:
    _, thresh = cv2.threshold(
        blurred, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh

def deskew(thresh: np.ndarray) -> np.ndarray:
    inverted = cv2.bitwise_not(thresh)
    coords = np.column_stack(np.where(inverted > 0))

    if len(coords) == 0:
        return thresh

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle

    (h, w) = thresh.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(
        thresh, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return deskewed

def run_ocr(pil_image: Image.Image, psm: int = 3) -> dict:
    img_array = np.array(pil_image)

    gray     = to_grayscale(img_array)
    blurred  = apply_blur(gray)
    thresh   = apply_threshold(blurred)
    deskewed = deskew(thresh)

    config = f"--oem 3 --psm {psm}"

    text = pytesseract.image_to_string(deskewed, config=config).strip()

    data = pytesseract.image_to_data(
        deskewed,
        config=config,
        output_type=pytesseract.Output.DICT
    )
    confidences = [
        int(c) for c in data["conf"]
        if str(c).lstrip("-").isdigit() and int(c) >= 0
    ]
    mean_conf = float(np.mean(confidences)) if confidences else 0.0

    return {
        "original": img_array,
        "gray":     gray,
        "thresh":   thresh,
        "deskewed": deskewed,
        "text":     text,
        "confidence": mean_conf,
    }
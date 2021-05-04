import os
import cv2
import pytesseract

def ocr_text(filename):
    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    img = cv2.imread(os.path.join("static/uploads", filename))
    text = pytesseract.image_to_string(img)
    return text


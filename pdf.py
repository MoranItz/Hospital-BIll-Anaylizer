import pytesseract
from PIL import Image, ImageOps
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
RENDER_DPI = 300
OCR_CONFIG = '--oem 3 --psm 6 -c preserve_interword_spaces=1'

def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    scale = RENDER_DPI / 72
    matrix = fitz.Matrix(scale, scale)
    for page in doc:
        pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csGRAY, alpha=False)
        image_path = f"page_{page.number}.png"
        pix.save(image_path)
        images.append(image_path)
    doc.close()
    return images


def image_to_text(images):
    text = ""
    for image_path in images:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            img = ImageOps.autocontrast(img.convert("L"))
            text += pytesseract.image_to_string(img, config=OCR_CONFIG)
    return text
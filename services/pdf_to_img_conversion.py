from pdf2image import convert_from_bytes
from PIL import Image
from typing import List
import os

poppler_path = os.getenv("POPPLER_PATH", r"D:/python/python modules/third party modules/poppler/poppler-25.12.0/Library/bin")

def pdf_to_image(pdf_bytes: bytes) -> List[Image.Image]:

    images = convert_from_bytes(pdf_bytes, dpi=300, fmt="png", poppler_path=poppler_path)
    return images
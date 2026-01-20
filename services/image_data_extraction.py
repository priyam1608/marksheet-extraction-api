import pytesseract
from pytesseract import Output
from PIL import Image
from typing import Dict

def extract_text_from_image(image: Image.Image) -> Dict:
    
    ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT)
    
    words = []
    confidences = []

    for i in range(len(ocr_data["text"])):
        text = ocr_data["text"][i].strip()
        conf = int(ocr_data["conf"][i])

        if (text and conf>0):
            words.append(text)
            confidences.append(conf)

    full_text = " ".join(words)
    avg_confidence = sum(confidences)/len(confidences) if confidences else 0

    return {
        "page": 1,
        "text": full_text,
        "ocr_confidence":round(avg_confidence/100, 2)
    }

def extract_text_from_images(images):
    page_results = []

    for page_no, image in enumerate(images, start=1):
        result = extract_text_from_image(image)
        page_results.append({
            "page": page_no,
            "text": result["text"],
            "ocr_confidence": result["ocr_confidence"]
        })

    return page_results
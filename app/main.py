from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from services.pdf_to_img_conversion import pdf_to_image
from PIL import Image
import io

from services.image_data_extraction import extract_text_from_image, extract_text_from_images
from llm.model import build_graph

app = FastAPI(title="Marksheet Extraction API")

graph = build_graph()

allowed_types = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png"
}

max_file_size = 10 * 1024 * 1024    # 10mb

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, JPG, PNG allowed.")

    contents = await file.read()

    if(len(contents) > max_file_size):
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit.")

    
    if file.content_type == "application/pdf":
        images = pdf_to_image(contents)
    else:
        image = Image.open(io.BytesIO(contents))
        images = [image]

    ocr_pages = extract_text_from_images(images)

    if not ocr_pages:
        raise HTTPException(status_code=422, detail="Unable to extract text from document")
    
    initial_state = {
        "ocr_pages":ocr_pages
    }

    result_state = graph.invoke(initial_state)

    return JSONResponse(content=result_state["final_result"])
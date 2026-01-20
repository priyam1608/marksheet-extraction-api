from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from .schemas import MarksheetExtraction

def connect_with_model(): 
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=GOOGLE_API_KEY)

    structured_model = model.with_structured_output(MarksheetExtraction)
    return structured_model

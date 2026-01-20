# Marksheet Extraction API

An intelligent document processing API that extracts structured data from marksheets using OCR and LLM-powered extraction.

## Features

- **PDF & Image Support**: Process both PDF and image files (JPG, PNG)
- **OCR Integration**: Extract text using Tesseract OCR
- **LLM Extraction**: Use Google Gemini for intelligent data extraction
- **Data Validation**: Automatic validation and normalization of extracted data
- **Confidence Scoring**: Get confidence scores for extracted information
- **FastAPI**: Modern async API with automatic documentation

## Project Structure

```
├── app/
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── llm/
│   ├── __init__.py
│   ├── connector.py            # LLM model connection
│   ├── model.py                # LangGraph workflow
│   ├── schemas.py              # Pydantic data models
│   └── state_logic.py          # Workflow node logic
├── services/
│   ├── __init__.py
│   ├── pdf_to_img_conversion.py # PDF processing
│   ├── image_data_extraction.py # OCR extraction
│   └── utils.py                # Utility functions
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.9+
- Tesseract OCR installed
- Poppler (for PDF conversion)

### Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd Marksheet\ Extraction
```

2. **Create virtual environment**:
```bash
python -m venv trestle_env
trestle_env\Scripts\activate  # Windows
# or
source trestle_env/bin/activate  # Linux/Mac
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set environment variables**:
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_api_key
POPPLER_PATH=path/to/poppler/bin  # Optional, defaults to configured path
```

## Usage

### Start the API
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Extract Marksheet
**POST** `/extract`

**Request**: Upload a PDF or image file
```bash
curl -X POST "http://127.0.0.1:8000/extract" \
  -F "file=@marksheet.pdf"
```

**Response**: Extracted and validated marksheet data with confidence scores

## Supported File Types
- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)

**Max File Size**: 10 MB

## Technologies Used

- **FastAPI**: Web framework
- **LangGraph**: Workflow orchestration
- **Langchain**: LLM integration
- **Google Gemini API**: LLM model
- **Tesseract**: OCR engine
- **pdf2image**: PDF processing
- **Pydantic**: Data validation

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Invalid file type or size exceeds limit
- `422`: Unable to extract text from document
- `500`: Internal server error

## Development

### Project Setup
```bash
git clone <repo-url>
cd Marksheet\ Extraction
python -m venv trestle_env
trestle_env\Scripts\activate
pip install -r requirements.txt
```

### Running Tests
```bash
pytest
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

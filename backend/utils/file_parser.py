import io
import fitz  # PyMuPDF
import docx

def parse_file_content(filename: str, file_bytes: bytes) -> str:
    """
    Extracts text from PDF or DOCX file bytes.
    """
    text = ""
    filename = filename.lower()

    try:
        if filename.endswith(".pdf"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
        elif filename.endswith(".docx"):
            doc = docx.Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing file: {e}")
        pass

    return text.strip()

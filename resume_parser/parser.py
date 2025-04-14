import PyPDF2
from docx import Document

def extract_resume_text(file):
    try:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            text = " ".join(paragraph.text for paragraph in doc.paragraphs)
        elif file.type == "text/plain":
            text = file.getvalue().decode("utf-8")
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        text = ""
        print(f"Error extracting text: {str(e)}")
    return text

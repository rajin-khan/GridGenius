import pdfplumber
import docx
from bs4 import BeautifulSoup

def extract_text_from_file(file_path):
    ext = file_path.split('.')[-1].lower()
    text = ""

    try:
        if ext == "txt":
            with open(file_path, 'r', encoding="utf-8") as f:
                text = f.read()

        elif ext == "pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

        elif ext == "docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif ext in ["html", "htm"]:
            with open(file_path, 'r', encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                text = soup.get_text()

        elif ext == "md":
            with open(file_path, 'r', encoding="utf-8") as f:
                text = f.read()

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return text.strip()

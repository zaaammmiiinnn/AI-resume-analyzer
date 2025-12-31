import PyPDF2
import re


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()


def clean_text(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    return text.lower()


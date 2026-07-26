import fitz
import re


def extract_text(pdf_path):
    """
    Extract all text from the uploaded PDF.
    """

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception:
        return ""

    return text


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if (
            len(line) > 3
            and "@" not in line
            and "resume" not in line.lower()
            and "curriculum" not in line.lower()
        ):
            return line

    return "Not Found"


def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    match = re.search(
        r"(\+91[\-\s]?)?[6-9]\d{9}",
        text,
    )

    if match:
        return match.group()

    return "Not Found"


def extract_github(text):

    match = re.search(
        r"(https?://)?(www\.)?github\.com/[^\s]+",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group()

    return "Not Found"


def extract_linkedin(text):

    match = re.search(
        r"(https?://)?(www\.)?linkedin\.com/[^\s]+",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group()

    return "Not Found"


def word_count(text):
    return len(text.split())


def page_count(pdf_path):

    try:
        doc = fitz.open(pdf_path)
        pages = len(doc)
        doc.close()
        return pages

    except Exception:
        return 0
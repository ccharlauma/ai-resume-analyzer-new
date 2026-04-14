from PyPDF2 import PdfReader

# ✅ FUNCTION 1 (YOU LOST THIS BEFORE)
def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# ✅ FUNCTION 2 (UPDATED SKILL FILTER)
def extract_keywords(text):
    text = text.lower()

    skills = {
        "python","java","c++","javascript","html","css","sql",
        "react","node","flask","django","mongodb","mysql",
        "aws","docker","kubernetes","git","linux",
        "machine","learning","ai","data","analysis","pandas",
        "numpy","tensorflow","api","backend","frontend",
        "devops","cloud","testing","automation"
    }

    words = text.split()
    keywords = set()

    for word in words:
        word = word.strip(",.()[]{}")

        if word in skills:
            keywords.add(word)

    return keywords
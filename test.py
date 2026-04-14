from utils import extract_text, extract_keywords

def analyze():
    resume = extract_text("resume.pdf.pdf")  # keep your working filename
    job = "python java sql"

    resume_words = extract_keywords(resume)
    job_words = extract_keywords(job)

    matched = resume_words & job_words
    missing = job_words - resume_words

    score = (len(matched) / len(job_words)) * 100

    print("\n===== SMART RESULT =====")
    print("Score:", round(score, 2), "%")
    print("\nMatched Keywords:", matched)
    print("\nMissing Keywords:", missing)

analyze()
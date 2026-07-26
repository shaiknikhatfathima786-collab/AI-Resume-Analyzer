from flask import Flask, render_template, request
import os

from resume_parser import (
    extract_text,
    extract_name,
    extract_email,
    extract_phone,
    extract_github,
    extract_linkedin,
    word_count,
    page_count,
)

from skills import skills

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a PDF."

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    resume_text = extract_text(filepath)

    if resume_text == "":
        return "Unable to read this PDF."

    # Resume Details
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    github = extract_github(resume_text)
    linkedin = extract_linkedin(resume_text)

    words = word_count(resume_text)
    pages = page_count(filepath)

    matched = []
    missing = []

    text = resume_text.lower()

    for skill in skills:

        if skill.lower() in text:
            matched.append(skill)

        else:
            missing.append(skill)

    ats_score = round((len(matched) / len(skills)) * 100)

    suggestions = []

    if ats_score < 40:

        suggestions.append("Add more technical skills.")
        suggestions.append("Mention projects clearly.")
        suggestions.append("Include certifications.")
        suggestions.append("Add GitHub profile.")
        suggestions.append("Improve resume formatting.")

    elif ats_score < 70:

        suggestions.append("Add more relevant keywords.")
        suggestions.append("Improve project descriptions.")
        suggestions.append("Mention internships.")
        suggestions.append("Include LinkedIn profile.")

    else:

        suggestions.append("Excellent ATS Score.")
        suggestions.append("Keep adding latest projects.")
        suggestions.append("Keep certifications updated.")

    return render_template(

        "result.html",

        ats_score=ats_score,

        matched_skills=matched,

        missing_skills=missing,

        suggestions=suggestions,

        name=name,
        email=email,
        phone=phone,
        github=github,
        linkedin=linkedin,

        words=words,
        pages=pages

    )


if __name__ == "__main__":
    app.run(debug=True)
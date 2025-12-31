from flask import Flask, render_template, request
import os

from utils import extract_text_from_pdf, clean_text
from skills import SKILLS

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files["resume"]
        job_desc = request.form["job_desc"].lower()

        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
        resume.save(resume_path)

        resume_text = extract_text_from_pdf(resume_path)
        resume_text = clean_text(resume_text)

        matched_skills = []
        for skill in SKILLS:
            if skill in resume_text and skill in job_desc:
                matched_skills.append(skill)

        match_percentage = int((len(matched_skills) / len(SKILLS)) * 100)

        return render_template(
            "result.html",
            matched_skills=matched_skills,
            match_percentage=match_percentage
        )

    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True)

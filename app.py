from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from bson import ObjectId
from models.database import users, resumes
from utils.ai_analyzer import analyze_resume
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text
from dotenv import load_dotenv
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.database import users

import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY"
)


def is_logged_in():
    return "user_id" in session


@app.route("/")
def home():

    if not is_logged_in():
        return redirect("/login")

    user_reports = list(

        resumes.find({

            "user_id":
            session["user_id"]

        })

    )

    total_reports = len(
        user_reports
    )

    best_resume = max(

        [r.get(
            "resume_score",
            0
        ) for r in user_reports],

        default=0

    )

    best_ats = max(

        [r.get(
            "ats_score",
            0
        ) for r in user_reports],

        default=0

    )

    recent_reports = user_reports[-5:]

    return render_template(

        "dashboard.html",

        username=session["username"],

        total_reports=total_reports,

        best_resume=best_resume,

        best_ats=best_ats,

        recent_reports=recent_reports

    )

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        existing_user = users.find_one(
            {"email": email}
        )

        if existing_user:
            return "Email already exists"

        users.insert_one({

            "username": username,

            "email": email,

            "password":
            generate_password_hash(
                password
            )

        })

        return redirect("/login")

    return render_template(
        "register.html"
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        user = users.find_one({
            "email": email
        })

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = str(
                user["_id"]
            )

            session["username"] = (
                user["username"]
            )

            return redirect("/")

        return "Invalid credentials"

    return render_template(
        "login.html"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route(
    "/upload",
    methods=["POST"]
)
def upload_resume():

    if not is_logged_in():
        return redirect("/login")

    file = request.files["resume"]

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        "static/uploads",
        filename
    )

    file.save(filepath)

    resume_text = extract_text(
        filepath
    )

    analysis = analyze_resume(
        resume_text
    )

    resumes.insert_one({

        "user_id": session["user_id"],

        "filename": filename,

        "resume_score":
            analysis.get(
                "resume_score",
                0
            ),

        "ats_score":
            analysis.get(
                "ats_score",
                0
            ),

        "analysis": analysis

    })

    return render_template(

        "upload.html",

        analysis=analysis,

        resume_text=resume_text

    )
@app.route("/history")
def history():

    if not is_logged_in():
        return redirect("/login")

    history_data = resumes.find({

        "user_id": session["user_id"]

    })

    return render_template(

        "history.html",

        history_data=history_data

    )

@app.route("/delete-report/<report_id>")
def delete_report(report_id):

    if not is_logged_in():
        return redirect("/login")

    resumes.delete_one({

        "_id": ObjectId(report_id)

    })

    return redirect("/history")

if __name__ == "__main__":
    app.run(debug=True)
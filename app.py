from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
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

    return render_template(
        "dashboard.html",
        username=session["username"]
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

    return render_template(
        "upload.html",
        resume_text=resume_text
    )

if __name__ == "__main__":
    app.run(debug=True)
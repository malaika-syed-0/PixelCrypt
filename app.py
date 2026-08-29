from flask import Flask, render_template, request, send_file, session, redirect
from crypto_engine import encrypt_message, decrypt_message
from stego_engine import hide_message, reveal_message
from datetime import datetime
from flask_bcrypt import Bcrypt
from database import init_db

import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "StegoApp_2026")

bcrypt = Bcrypt(app)
init_db()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"


# =========================
# HOME
# =========================

@app.route("/")
def home():

    if "user" in session:
        return redirect("/dashboard")

    return render_template("landing.html")
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

# =========================
# REGISTER
# =========================
@app.route("/register")
def register_page():
    return render_template("register.html")
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Email validation
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):

        return render_template(

            "popup.html",

            title="❌ Invalid Email",

            message="Please enter a valid email address.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/register"

        )

    # Username validation
    if len(username) < 4:

        return render_template(

            "popup.html",

            title="❌ Invalid Username",

            message="Username must contain at least 4 characters.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/register"

        )

    # Password validation
    if (

        len(password) < 8

        or not re.search(r"[A-Z]", password)

        or not re.search(r"[a-z]", password)

        or not re.search(r"\d", password)

    ):

        return render_template(

            "popup.html",

            title="❌ Weak Password",

            message="Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/register"

        )

    # Confirm password
    if password != confirm_password:

        return render_template(

            "popup.html",

            title="❌ Password Mismatch",

            message="Passwords do not match.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/register"

        )

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    conn = sqlite3.connect("users.db")

    existing = conn.execute(

        """
        SELECT *
        FROM users
        WHERE username=? OR email=?
        """,

        (
            username,
            email
        )

    ).fetchone()

    if existing:

        conn.close()

        return render_template(

            "popup.html",

            title="❌ Account Already Exists",

            message="Username or email already exists.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/register"

        )

    conn.execute(

        """
        INSERT INTO users
        (username,email,password)

        VALUES(?,?,?)
        """,

        (
            username,
            email,
            hashed_password
        )

    )

    conn.commit()
    conn.close()

    return render_template(

        "popup.html",

        title="✅ Registration Successful",

        message="Your PixelCrypt account has been created successfully.",

        color="#00ff99",

        shadow="rgba(0,255,153,.35)",

        back="/login"

    )
# =========================
# LOGIN
# =========================

@app.route("/login")
def login_page():

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"].strip()
    password = request.form["password"]

    conn = sqlite3.connect("users.db")

    user = conn.execute(

        """
        SELECT *
        FROM users
        WHERE username=?
        """,

        (username,)

    ).fetchone()

    conn.close()

    if user and bcrypt.check_password_hash(

        user[3],
        password

    ):

        session["user"] = username

        return redirect("/dashboard")

    return render_template(

        "popup.html",

        title="❌ Login Failed",

        message="Invalid username or password.",

        color="#ff5555",

        shadow="rgba(255,85,85,.35)",

        back="/login"

    )
# =========================
# SETTINGS PAGE
# =========================

@app.route("/settings")
def settings():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")

    conn.row_factory = sqlite3.Row

    user = conn.execute(

        """
        SELECT username,email
        FROM users
        WHERE username=?
        """,

        (session["user"],)

    ).fetchone()

    conn.close()

    return render_template(

        "settings.html",

        user=user

    )
@app.route("/settings", methods=["POST"])
def update_settings():

    if "user" not in session:
        return redirect("/login")

    username = request.form["username"].strip()

    email = request.form["email"].strip()

    current_password = request.form["current_password"]

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]

    conn = sqlite3.connect("users.db")

    conn.row_factory = sqlite3.Row

    user = conn.execute(

        """
        SELECT *
        FROM users
        WHERE username=?
        """,

        (session["user"],)

    ).fetchone()
        # Check if email already exists for another user
    existing = conn.execute(

        """
        SELECT *
        FROM users
        WHERE email=? AND username!=?
        """,

        (
            email,
            session["user"]
        )

    ).fetchone()

    if existing:

        conn.close()

        return render_template(

            "popup.html",

            title="❌ Email Already Exists",

            message="This email address is already being used by another account.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/settings"

        )

    # User wants to change password
    if new_password or confirm_password:

        if not bcrypt.check_password_hash(

            user["password"],
            current_password

        ):

            conn.close()

            return render_template(

                "popup.html",

                title="❌ Incorrect Password",

                message="Your current password is incorrect.",

                color="#ff5555",

                shadow="rgba(255,85,85,.35)",

                back="/settings"

            )

        if new_password != confirm_password:

            conn.close()

            return render_template(

                "popup.html",

                title="❌ Password Mismatch",

                message="New passwords do not match.",

                color="#ff5555",

                shadow="rgba(255,85,85,.35)",

                back="/settings"

            )

        if (

            len(new_password) < 8

            or not re.search(r"[A-Z]", new_password)

            or not re.search(r"[a-z]", new_password)

            or not re.search(r"\d", new_password)

        ):

            conn.close()

            return render_template(

                "popup.html",

                title="❌ Weak Password",

                message="Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number.",

                color="#ff5555",

                shadow="rgba(255,85,85,.35)",

                back="/settings"

            )

        hashed_password = bcrypt.generate_password_hash(

            new_password

        ).decode("utf-8")

    else:

        hashed_password = user["password"]
    conn.execute(

        """
        UPDATE users

        SET

        username=?,

        email=?,

        password=?

        WHERE username=?

        """,

        (

            username,

            email,

            hashed_password,

            session["user"]

        )

    )

    conn.commit()

    conn.close()

    # Update session if username changed
    session["user"] = username

    return render_template(

        "popup.html",

        title="✅ Settings Updated",

        message="Your account settings have been updated successfully.",

        color="#00ff99",

        shadow="rgba(0,255,153,.35)",

        back="/dashboard"

    )
    # =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect("users.db")

    conn.row_factory = sqlite3.Row

    history = conn.execute(

        """
        SELECT *

        FROM history

        WHERE username=?

        ORDER BY id DESC
        """,

        (session["user"],)

    ).fetchall()

    conn.close()

    return render_template(

        "history.html",

        history=history

    )
# =========================
# ENCODE
# =========================

@app.route("/encode", methods=["GET", "POST"])
def encode():

    if request.method == "GET":
        return render_template("encode.html")

    image = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    encrypted_message = encrypt_message(
        message,
        password
    )

    # Get original filename
    original_filename = image.filename

    # Remove extension
    filename = os.path.splitext(original_filename)[0]

    # Create encoded filename
    output_filename = f"{filename}_encoded.png"

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        original_filename
    )

    image.save(upload_path)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    hide_message(
        upload_path,
        encrypted_message,
        output_path
    )

    session["encoded_file"] = output_filename
    conn = sqlite3.connect("users.db")
    conn.execute(
        """
        INSERT INTO history
        (username,action,image_name,date_time,status)
        VALUES(?,?,?,?,?)
        """,
        (
            session["user"],
            "Encode",
            output_filename,
            datetime.now().strftime("%d %b %Y %I:%M %p"),
            "Success"
        )
        
    )
    conn.commit()
    conn.close()
    return render_template(

        "popup.html",

        title="✅ Message Hidden",

        message="Your secret message has been encrypted and hidden successfully. Click OK to go back to the encoding screen, then click Download Image at the bottom of screen to save the encoded PNG.",

        color="#00ff99",

        shadow="rgba(0,255,153,.35)",

        back="/encode"

    )


# =========================
# DOWNLOAD
# =========================

@app.route("/download")
def download():

    filename = session.get("encoded_file")

    if not filename:

        return render_template(

            "popup.html",

            title="⚠ No Encoded Image",

            message="There is no encoded image available to download.\n\nPlease hide a secret message first.",

            color="#ffc107",

            shadow="rgba(255,193,7,.35)",

            back="/encode"

        )

    hidden_image = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    response = send_file(

        hidden_image,

        as_attachment=True,

        download_name=filename

    )

    session.pop("encoded_file", None)

    return response
# =========================
# DECODE PAGE
# =========================

@app.route("/decode_page")
def decode_page():

    return render_template("decode.html")


# =========================
# DECODE
# =========================

@app.route("/decode", methods=["POST"])
def decode():

    image = request.files["image"]
    password = request.form["password"]

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        image.filename
    )

    image.save(upload_path)

    # Check whether the image contains a hidden message
    try:

        encrypted_message = reveal_message(upload_path)

    except IndexError:

        return render_template(

            "popup.html",

            title="⚠ No Hidden Message",

            message="This PNG image does not contain any hidden secret message.",

            color="#ffc107",

            shadow="rgba(255,193,7,.35)",

            back="/decode_page"

        )

    # Check password
    try:

        original_message = decrypt_message(
            encrypted_message,
            password
        )

    except Exception:

        return render_template(

            "popup.html",

            title="❌Decryption Failed ",

            message="The password is incorrect, or the image has been modified or corrupted.",

            color="#ff5555",

            shadow="rgba(255,85,85,.35)",

            back="/decode_page"

        )    
        # Save Decode History

    conn = sqlite3.connect("users.db")

    conn.execute(

        """
        INSERT INTO history
        (username, action, image_name, date_time, status)
        VALUES (?, ?, ?, ?, ?)
        """,

        (
            session["user"],
            "Decode",
            image.filename,
            datetime.now().strftime("%d %b %Y %I:%M %p"),
            "Success"
        )

    )

    conn.commit()

    conn.close()

    # Success

    return render_template(

        "popup.html",

        title="✅ Secret Message Recovered",

        message=original_message,

        color="#00ff99",

        shadow="rgba(0,255,153,.35)",

        back="/dashboard"

    )
# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
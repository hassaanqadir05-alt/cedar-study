import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key-2026")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_daily_quote():
    """Bonus 5%: Third-Party External API Integration"""
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=3)
        if res.status_code == 200:
            data = res.json()[0]
            return f'"{data["q"]}" — {data["a"]}'
    except Exception:
        pass
    return '"Success is the sum of small efforts, repeated day in and day out." — Robert Collier'


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        existing = supabase.table("users").select("*").eq("username", username).execute()
        if existing.data:
            flash("Username already taken. Please choose another.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        supabase.table("users").insert({
            "username": username,
            "password_hash": hashed_pw
        }).execute()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        result = supabase.table("users").select("*").eq("username", username).execute()
        if result.data:
            user = result.data[0]
            if check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # READ operation: fetch only the logged-in user's tasks
    response = supabase.table("tasks").select("*").eq("user_id", session["user_id"]).order("id", desc=True).execute()
    tasks = response.data
    quote = get_daily_quote()

    return render_template("dashboard.html", tasks=tasks, username=session["username"], quote=quote)


@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # CREATE operation
    title = request.form.get("title").strip()
    subject = request.form.get("subject").strip()
    priority = request.form.get("priority")

    if title and subject:
        supabase.table("tasks").insert({
            "user_id": session["user_id"],
            "title": title,
            "subject": subject,
            "priority": priority,
            "is_completed": False
        }).execute()

    return redirect(url_for("dashboard"))


@app.route("/toggle_task/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # UPDATE operation
    current = supabase.table("tasks").select("is_completed").eq("id", task_id).eq("user_id", session["user_id"]).execute()
    if current.data:
        new_status = not current.data[0]["is_completed"]
        supabase.table("tasks").update({"is_completed": new_status}).eq("id", task_id).eq("user_id", session["user_id"]).execute()

    return redirect(url_for("dashboard"))


@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # DELETE operation
    supabase.table("tasks").delete().eq("id", task_id).eq("user_id", session["user_id"]).execute()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
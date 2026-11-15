# CedarStudy — Student Task & Study Manager

A full-stack web application built for the Fall 2026 Full-Stack Engineering Capstone at Cedar College. CedarStudy helps students organize coursework, track assignments by subject and priority, and manage study tasks with persistent cloud storage.

**Live Application:** [https://cedar-study.vercel.app](https://cedar-study.vercel.app)

---

## Features

* **User Authentication:** Secure account registration and login with hashed passwords (`Werkzeug`) and server-side Flask sessions.
* **Task Management (CRUD):** Create, view, and manage study tasks organized by subject and priority level.
* **Persistent Cloud Database:** All user accounts and task records are stored in PostgreSQL via Supabase.
* **Serverless Deployment:** Deployed on Vercel using Python serverless functions (`@vercel/python`).

---

## Tech Stack

* **Backend:** Python 3, Flask 3.0
* **Database & API:** Supabase (PostgreSQL + REST API via `supabase-py`)
* **Frontend:** HTML5, CSS3 (Jinja2 templates)
* **Deployment:** Vercel (Serverless Functions)

---

## Project Structure

```text
cedar-study/
└── cedar-capstone/
    ├── api/
    │   └── index.py          # Main Flask application and API routes
    ├── static/
    │   └── style.css         # Application styling
    ├── templates/
    │   ├── login.html        # User login page
    │   ├── register.html     # User registration page
    │   └── dashboard.html    # Main task management dashboard
    ├── .gitignore            # Excludes .env, __pycache__, and virtual environments
    ├── requirements.txt      # Python dependencies
    └── vercel.json           # Vercel serverless routing configuration

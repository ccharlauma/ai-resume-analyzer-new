from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os, sqlite3, pdfplumber

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS history (username TEXT, score INTEGER, matched TEXT, missing TEXT)")

    conn.commit()
    conn.close()

init_db()

# ---------------- ROOT ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if action == "login":
            if user and check_password_hash(user[1], password):
                session["user"] = username
                return redirect("/dashboard")
            else:
                error = "Invalid credentials"

        elif action == "register":
            if user:
                error = "User exists"
            else:
                hashed = generate_password_hash(password)
                c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
                conn.commit()
                session["user"] = username
                return redirect("/dashboard")

        conn.close()

    return render_template("login.html", error=error)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    result = None
    history = []

    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_description"]

        if file.filename == "":
            return redirect("/dashboard")

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        resume = text.lower()

        skills = ["python","react","node","api","docker","html","css","sql"]

        matched = [s for s in skills if s in resume]
        missing = [s for s in skills if s not in resume]

        job_words = job_desc.lower().split()
        match_count = sum(1 for word in job_words if word in resume)

        score = int((match_count / len(job_words)) * 100) if job_words else 0

        # AI REMOVED (SAFE)
        ai_text = "AI temporarily disabled"

        jobs = []
        if "python" in matched:
            jobs.append("Backend Developer")
        if "react" in matched:
            jobs.append("Frontend Developer")
        if "sql" in matched:
            jobs.append("Data Analyst")

        result = {
            "score": score,
            "matched": matched,
            "missing": missing,
            "jobs": jobs,
            "ai": ai_text
        }

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO history VALUES (?, ?, ?, ?)",
            (session["user"], score, ",".join(matched), ",".join(missing))
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT score, matched FROM history WHERE username=?", (session["user"],))
    history = c.fetchall()
    conn.close()

    return render_template("index.html", user=session["user"], result=result, history=history)

# ---------------- ANALYTICS ----------------
@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT score FROM history WHERE username=?", (session["user"],))
    data = c.fetchall()

    conn.close()

    scores = [int(i[0]) for i in data]

    return render_template("analytics.html", scores=scores)

# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")
    return render_template("profile.html", user=session["user"])

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
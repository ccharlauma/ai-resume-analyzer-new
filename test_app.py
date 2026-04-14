from flask import Flask, request
import sqlite3

app = Flask(__name__)

# create DB
conn = sqlite3.connect("test.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()
conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        action = request.form.get("action")

        print("FORM:", request.form)
        print("ACTION:", action)

        conn = sqlite3.connect("test.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()

        print("USER FROM DB:", user)

        if action == "register":
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            return "REGISTERED ✅"

        elif action == "login":
            if user and user[1] == password:
                return "LOGIN SUCCESS ✅"
            else:
                return "LOGIN FAILED ❌"

        conn.close()

    return '''
    <form method="POST">
        <input name="username" placeholder="username">
        <input name="password" placeholder="password">
        <button name="action" value="login">Login</button>
        <button name="action" value="register">Register</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
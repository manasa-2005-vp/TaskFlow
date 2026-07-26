from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# MySQL connection
db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)


@app.route("/")
def home():
    return "TaskFlow is working!"

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """, (name, email, hashed_password))

        db.commit()
        cursor.close()

        return redirect("/login")

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (session["user_id"],))

    tasks = cursor.fetchall()

    cursor.close()

    return render_template(
        "dashboard.html",
        tasks=tasks
    )
@app.route("/add_task", methods=["GET", "POST"])
def add_task():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        due_date = request.form["due_date"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO tasks
            (user_id, title, description, priority, status, due_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session["user_id"],
            title,
            description,
            priority,
            status,
            due_date if due_date else None
        ))

        db.commit()
        cursor.close()

        return redirect("/dashboard")

    return render_template("add_task.html")
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    # Make sure this task belongs to the logged-in user
    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE task_id = %s AND user_id = %s
    """, (task_id, session["user_id"]))

    task = cursor.fetchone()

    if task is None:
        cursor.close()
        return "Task not found", 404

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        due_date = request.form["due_date"]

        cursor.execute("""
            UPDATE tasks
            SET title = %s,
                description = %s,
                priority = %s,
                status = %s,
                due_date = %s
            WHERE task_id = %s AND user_id = %s
        """, (
            title,
            description,
            priority,
            status,
            due_date if due_date else None,
            task_id,
            session["user_id"]
        ))

        db.commit()
        cursor.close()

        return redirect("/dashboard")

    cursor.close()

    return render_template(
        "edit_task.html",
        task=task
    )
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE task_id = %s AND user_id = %s
    """, (
        task_id,
        session["user_id"]
    ))

    db.commit()
    cursor.close()

    return redirect("/dashboard")
@app.route("/api/tasks")
def api_tasks():

    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT task_id, title, description,
               priority, status, due_date, created_at
        FROM tasks
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (session["user_id"],))

    tasks = cursor.fetchall()
    cursor.close()

    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)
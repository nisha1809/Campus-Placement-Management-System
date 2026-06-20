import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, branch, cgpa FROM student"
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students
    )


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():

    if request.method == 'POST':
        print("POST request received")

        email = request.form['email']
        password = request.form['password']
        print("Email:",email)
        print("Password:",password)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM student WHERE email=%s AND password=%s",
            (email, password)
        )

        student = cursor.fetchone()
        print("database result:", student)

        conn.close()

        if student:
            return render_template(
                "student_dashboard.html",
                student=student
            )
        else:
            return "Invalid Email or Password"

    return render_template(
        "student_login.html"
    )


@app.route('/admin-login')
def admin_login():
    return render_template(
        'admin_login.html'
    )


@app.route('/student-dashboard')
def student_dashboard():
    return render_template(
        'student_dashboard.html'
    )


@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template(
        'admin_dashboard.html'
    )


if __name__ == '__main__':
    app.run(debug=True)
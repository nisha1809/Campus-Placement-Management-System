
import mysql.connector
from flask import Flask,render_template
app=Flask(__name__)
@app.route("/")
def home():
    conn =mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="18092005",
                                  database="placement_management")
    cursor=conn.cursor()
    cursor.execute("select name,branch,cgpa from student")
    students=cursor.fetchall()
    output=""
    for student in students:
        output+=f"Name: {student[0]}, Branch: {student[1]}, CGPA: {student[2]}<br>"
        conn.close()
        return render_template("index.html",students=students)
if __name__=='__main__':
    app.run(debug=True)
    @app.route('/student-login')
    
    def student_login():
        return render_template('student_login.html')



@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')
        
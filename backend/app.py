import mysql.connector
from flask import Flask, render_template, request,session,redirect 
#session is used to store data of the current loged in user and can be used to access data across different routes
app = Flask(__name__)
app.secret_key = "placement_secret_key"#secret key is used to encrypt the session data and keep it secure


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
            session['student_id']=student[0]
            return render_template(
                "student_dashboard.html",
                student=student
            )
        else:
            return "Invalid Email or Password"

    return render_template(
        "student_login.html"
    )


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
    )

        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )

        admin = cursor.fetchone()

        conn.close()

        if admin:
            return redirect('/admin-dashboard')
        else:
            return "Invalid Admin Credentials"

    return render_template("admin_login.html")

@app.route('/student-dashboard')
def student_dashboard():
    return render_template(
        'student_dashboard.html'
    )

@app.route('/admin-dashboard')
def admin_dashboard():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    total_students = cursor.fetchone()[0]
    
    
    cursor.execute(
    """
    SELECT COUNT(*)
    FROM application
    WHERE status='Selected'
    """
)

    placed_students = cursor.fetchone()[0]
    
    cursor.execute(
    """
    SELECT COUNT(*)
    FROM application
    WHERE status='Eligible'
    """
)

    eligible_students = cursor.fetchone()[0]
    
    cursor.execute(
    """
    SELECT COUNT(*)
    FROM application
    WHERE status='Rejected'
    """
)

    rejected_students = cursor.fetchone()[0]
    
    if total_students > 0:

        placement_percentage = (
        placed_students / total_students
    ) * 100

    else:

        placement_percentage = 0
    

    cursor.execute("SELECT COUNT(*) FROM company")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM placement_drive")
    total_drives = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM application")
    total_applications = cursor.fetchone()[0]

    conn.close()

    return render_template(
    "admin_dashboard.html",

    total_students=total_students,
    total_companies=total_companies,
    total_drives=total_drives,
    total_applications=total_applications,

    placed_students=placed_students,
    eligible_students=eligible_students,
    rejected_students=rejected_students,

    placement_percentage=placement_percentage
)
@app.route('/student-details/<int:student_id>')
def student_details(student_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student WHERE student_id=%s",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "student_details.html",
        student=student
    )
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():

    if request.method == 'POST':

        phone = request.form['phone']
        skills = request.form['skills']
        resume = request.form['resume']
        address = request.form['address']
        linkedin = request.form['linkedin']
        github = request.form['github']

        student_id = session['student_id']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
    )

        cursor = conn.cursor()

        cursor.execute(
        """
        UPDATE student
        SET phone=%s,
            skills=%s,
            resume_link=%s,
            address=%s,
            linkedin_profile=%s,
            github_profile=%s
        WHERE student_id=%s
        """,
        (
            phone,
            skills,
            resume,
            address,
            linkedin,
            github,
            student_id
        )
    )

        conn.commit()

        conn.close()

        return "Profile Updated Successfully"

    return render_template(
        "edit_profile.html"
)
    
@app.route('/add-company', methods=['GET', 'POST'])
def add_company():

    if request.method == 'POST':

        company_name = request.form['company_name']
        role = request.form['role']
        package = request.form['package']
        eligibility_cgpa = request.form['eligibility_cgpa']
        location = request.form['location']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO company
            (company_name, role, package, eligibility_cgpa, location)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                company_name,
                role,
                package,
                eligibility_cgpa,
                location
            )
        )

        conn.commit()

        conn.close()

        return "Company Added Successfully"

    return render_template(
        "add_company.html"
    )
    
@app.route('/view-companies')
def view_companies():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM company"
    )

    companies = cursor.fetchall()

    conn.close()

    return render_template(
        "view_companies.html",
        companies=companies
    )
    
    
@app.route('/add-drive', methods=['GET', 'POST'])
def add_drive():

    if request.method == 'POST':

        company_id = request.form['company_id']
        drive_name = request.form['drive_name']
        role = request.form['role']
        package = request.form['package']
        eligibility_cgpa = request.form['eligibility_cgpa']
        eligible_branch = request.form['eligible_branch']
        
        
        deadline = request.form['deadline']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO placement_drive
            (company_id, drive_name, role, package, eligibility_cgpa,eligible_branch, deadline)
            VALUES (%s, %s, %s, %s, %s,%s, %s)
            """,
            (
                company_id,
                drive_name,
                role,
                package,
                eligibility_cgpa,
                deadline
            )
        )

        conn.commit()

        conn.close()

        return "Placement Drive Created Successfully"

    return render_template(
        "add_drive.html"
    )
    
    
@app.route('/view-drives')
def view_drives():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM placement_drive"
    )

    drives = cursor.fetchall()

    conn.close()

    return render_template(
        "view_drives.html",
        drives=drives
    )
    
@app.route('/student-drives')
def student_drives():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM placement_drive"
    )

    drives = cursor.fetchall()

    conn.close()

    return render_template(
        "student_drives.html",
        drives=drives
    )
    
    
@app.route('/apply/<int:drive_id>')
def apply(drive_id):

    student_id = session['student_id']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    # Check if student already applied

    cursor.execute(
        """
        SELECT *
        FROM application
        WHERE student_id=%s
        AND drive_id=%s
        """,
        (student_id, drive_id)
    )

    existing_application = cursor.fetchone()

    if existing_application:

        conn.close()

        return "You have already applied for this drive."

    # Fetch student CGPA and Branch

    cursor.execute(
        """
        SELECT cgpa, branch
        FROM student
        WHERE student_id=%s
        """,
        (student_id,)
    )

    student_data = cursor.fetchone()

    student_cgpa = float(student_data[0])
    student_branch = student_data[1]

    # Fetch required CGPA and Eligible Branch

    cursor.execute(
        """
        SELECT eligibility_cgpa, eligible_branch
        FROM placement_drive
        WHERE drive_id=%s
        """,
        (drive_id,)
    )

    drive_data = cursor.fetchone()

    required_cgpa = float(drive_data[0])
    eligible_branch = drive_data[1]

    # Automatic shortlisting

    if student_branch != eligible_branch:

        status = "Rejected"
        remarks = "Branch Not Eligible"

    elif student_cgpa < required_cgpa:

        status = "Rejected"
        remarks = "CGPA below eligibility criteria"

    else:

        status = "Eligible"
        remarks = "Eligible based on Branch and CGPA"

    # Insert application

    cursor.execute(
        """
        INSERT INTO application
        (student_id, drive_id, status, application_date, remarks)
        VALUES (%s, %s, %s, CURDATE(), %s)
        """,
        (
            student_id,
            drive_id,
            status,
            remarks
        )
    )

    conn.commit()

    conn.close()

    return f"""Application Submitted Successfully.<br></br>
Status:{status}<br></br>
Reason:{remarks}"""

    # Fetch student CGPA

   # Fetch student CGPA and Branch

    cursor.execute(
    """
    SELECT cgpa, branch
    FROM student
    WHERE student_id=%s
    """,
    (student_id,)
)

    student_data = cursor.fetchone()

    student_cgpa = float(student_data[0])
    student_branch = student_data[1]

# Fetch required CGPA and Eligible Branch

    cursor.execute(
    """
    SELECT eligibility_cgpa, eligible_branch
    FROM placement_drive
    WHERE drive_id=%s
    """,
    (drive_id,)
)

    drive_data = cursor.fetchone()

    required_cgpa = float(drive_data[0])
    eligible_branch = drive_data[1]

# Automatic shortlisting

    if student_branch != eligible_branch:

        status = "Rejected"
        remarks = "Branch Not Eligible"

    elif student_cgpa < required_cgpa:

        status = "Rejected"
        remarks = "CGPA below eligibility criteria"

    else:

        status = "Shortlisted"
        remarks = "Eligible based on Branch and CGPA"
        
        
    

    # Insert application

        cursor.execute(
        """
        INSERT INTO application
        (student_id, drive_id, status, application_date, remarks)
        VALUES (%s, %s, %s, CURDATE(), %s)
        """,
        (
            student_id,
            drive_id,
            status,
            remarks
        )
    )

    conn.commit()

    conn.close()

    return f"Application Submitted Successfully. Status: {status}.reason: {remarks}"


@app.route('/view-applications')
def view_applications():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            a.status,
            a.application_date,
            a.remarks,
            a.application_id
          

        FROM application a

        JOIN student
        ON a.student_id = student.student_id

        JOIN placement_drive
        ON a.drive_id = placement_drive.drive_id
        """
    )

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "view_applications.html",
        applications=applications
    )
    

    
'''@app.route('/approve/<int:application_id>')
def approve(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT remarks
        FROM application
        WHERE application_id=%s
        """,
        (application_id,)
    )

    remarks = cursor.fetchone()[0]

    if remarks == "Branch Not Eligible" or remarks == "CGPA below eligibility criteria":

        conn.close()

        return "Cannot approve. Student is not eligible."

    cursor.execute(
        """
        UPDATE application
        SET
        status='Shortlisted',
        remarks='Approved by Admin'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return "Application Approved Successfully"
    
    '''


'''@app.route('/reject/<int:application_id>')
def reject(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT remarks
        FROM application
        WHERE application_id=%s
        """,
        (application_id,)
    )

    remarks = cursor.fetchone()[0]

    if remarks == "Branch Not Eligible" or remarks == "CGPA below eligibility criteria":

        conn.close()

        return "Application already rejected automatically."

    cursor.execute(
        """
        UPDATE application
        SET
            status='Rejected',
            remarks='Rejected By Admin'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return "Application Rejected Successfully"
    
    '''


'''@app.route('/select/<int:application_id>')
def select_student(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    # Check current status

    cursor.execute(
        """
        SELECT status
        FROM application
        WHERE application_id=%s
        """,
        (application_id,)
    )

    status = cursor.fetchone()[0]

    if status == "Selected":

        conn.close()

        return "Student already selected."

    cursor.execute(
        """
        UPDATE application
        SET status='Selected',
            remarks='Selected By Admin'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return "Student Selected Successfully"



'''
@app.route('/my-applications')
def my_applications():

    student_id = session['student_id']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            placement_drive.drive_name,
            placement_drive.role,
            placement_drive.package,
            application.status,
            application.application_date,
            application.remarks

        FROM application

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.student_id = %s
        """,
        (student_id,)
    )

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )
    
#print(app.url_map)


@app.route('/student-register', methods=['GET', 'POST'])
def student_register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        branch = request.form['branch']
        cgpa = request.form['cgpa']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18092005",
            database="placement_management"
        )

        cursor = conn.cursor()

        # Check duplicate email

        cursor.execute(
            """
            SELECT *
            FROM student
            WHERE email=%s
            """,
            (email,)
        )

        existing_student = cursor.fetchone()

        if existing_student:

            conn.close()

            return "Email already registered."

        cursor.execute(
            """
            INSERT INTO student
            (name, email, password, phone, branch, cgpa)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                name,
                email,
                password,
                phone,
                branch,
                cgpa
            )
        )

        conn.commit()

        conn.close()

        return "Registration Successful"

    return render_template(
        "student_register.html"
    )
    
    
@app.route('/student-logout')
def student_logout():

    session.pop('student_id', None)

    return redirect('/student-login')


@app.route('/admin-logout')
def admin_logout():

    return redirect('/admin-login')


@app.route('/selected-students')
def selected_students():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            placement_drive.role,
            placement_drive.package

        FROM application

        JOIN student
        ON application.student_id = student.student_id

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.status='Selected'
        """
    )

    selected_students = cursor.fetchall()

    conn.close()

    return render_template(
        "selected_students.html",
        selected_students=selected_students
    )
    
    
@app.route('/delete-my-applications')
def delete_my_applications():

    student_id = session['student_id']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM application
        WHERE student_id=%s
        """,
        (student_id,)
    )

    conn.commit()

    conn.close()
@app.route('/delete-account')
def delete_account():

    student_id = session['student_id']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM application
        WHERE student_id=%s
        """,
        (student_id,)
    )

    cursor.execute(
        """
        DELETE FROM student
        WHERE student_id=%s
        """,
        (student_id,)
    )

    conn.commit()

    conn.close()

    session.clear()

    return redirect('/')

    return "All Applications Deleted Successfully"




@app.route('/aptitude-clear/<int:application_id>')
def aptitude_clear(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE application
        SET status='Aptitude Cleared',
            remarks='Cleared Aptitude Round'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return "Student Marked As Aptitude Cleared Successfully"


@app.route('/eligible-students')
def eligible_students():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            application.status,
            application.application_id

        FROM application

        JOIN student
        ON application.student_id = student.student_id

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.status='Eligible'
        """
    )

    students = cursor.fetchall()
    print("Eligible students fetched:", students)
    

    conn.close()

    return render_template(
        'eligible_students.html',
        students=students
    )
    
    
    
@app.route('/aptitude-cleared-students')
def aptitude_cleared_students():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            application.status,
            application.application_id

        FROM application

        JOIN student
        ON application.student_id = student.student_id

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.status='Aptitude Cleared'
        """
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'aptitude_cleared_students.html',
        students=students
    )
    
@app.route('/technical-clear/<int:application_id>')
def technical_clear(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE application
        SET status='Technical Cleared',
            remarks='Cleared Technical Round'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return redirect('/aptitude-cleared-students')


@app.route('/technical-cleared-students')
def technical_cleared_students():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            application.status,
            application.application_id

        FROM application

        JOIN student
        ON application.student_id = student.student_id

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.status='Technical Cleared'
        """
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'technical_cleared_students.html',
        students=students
    )
    
@app.route('/hr-clear/<int:application_id>')
def hr_clear(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE application
        SET status='HR Cleared',
            remarks='Cleared HR Round'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return "Student Marked As HR Cleared Successfully"



@app.route('/hr-cleared-students')
def hr_cleared_students():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student.name,
            student.branch,
            student.cgpa,
            placement_drive.drive_name,
            application.status,
            application.application_id

        FROM application

        JOIN student
        ON application.student_id = student.student_id

        JOIN placement_drive
        ON application.drive_id = placement_drive.drive_id

        WHERE application.status='HR Cleared'
        """
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'hr_cleared_students.html',
        students=students
    )
    
    
    
@app.route('/final-select/<int:application_id>')
def final_select(application_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="18092005",
        database="placement_management"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE application
        SET status='Selected',
            remarks='Final Selection Completed'
        WHERE application_id=%s
        """,
        (application_id,)
    )

    conn.commit()

    conn.close()

    return redirect('/selected-students')
if __name__ == '__main__':
    print("flask is starting...")
    print("reached app.run")
    app.run(debug=True)
USE placement_management;

//student table.
CREATE TABLE Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    branch VARCHAR(50),
    cgpa DECIMAL(3,2),
    password VARCHAR(100)
);
//company table.
CREATE TABLE Company (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    package DECIMAL(10,2),
    eligibility_cgpa DECIMAL(3,2),
    location VARCHAR(100)
);

//drive table.
CREATE TABLE Drive (
    drive_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    drive_date DATE,
    last_date_to_apply DATE,
    venue VARCHAR(100),

    FOREIGN KEY (company_id)
    REFERENCES Company(company_id)
);

//application table.
CREATE TABLE Application (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    drive_id INT,
    status VARCHAR(50),

    FOREIGN KEY (student_id)
    REFERENCES Student(student_id),

    FOREIGN KEY (drive_id)
    REFERENCES Drive(drive_id)
);

//ADMIN table.
CREATE TABLE Admin(
admin_id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(50) UNIQUE,
password VARCHAR(100)
);


//inserting values into the tables
INSERT INTO Admin (username,password) VALUES ('Admin','admin123');
select * from Admin;
INSERT INTO Drive(
company_id,drive_date,last_date_to_apply,venue)
VALUES
(1,'2025-09-01','2025-08-25','College Auditorium');
select * from Drive;

INSERT INTO Application 
(student_id,drive_id,status)
VALUES
(1,1,'Applied');
select * from Application;
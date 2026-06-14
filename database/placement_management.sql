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
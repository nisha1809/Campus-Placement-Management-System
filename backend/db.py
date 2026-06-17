
#connecting backend with the database
print("program started")
import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="18092005",
    database="placement_management"
)
print("Database connection successful")
#fetching data from the database
cursor=conn.cursor()
cursor.execute("SELECT * FROM STUDENT")
students=cursor.fetchall()
for student in students:
    print(student)
    print("data retrieved successfuly")
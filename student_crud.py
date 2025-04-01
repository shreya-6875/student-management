import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres.emlshwbeykjhzwmadxye"
DB_PASSWORD = "8768.P£d=mqt8IMTba"
DB_HOST = "aws-0-ap-south-1.pooler.supabase.com"
DB_PORT = "5432"

def db_connection():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        print("Connection successful!")
        return conn
    except Exception as e:
        print("Error Connecting to Database")
        print(e)
        return None

def create_table_departments():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    department_id SERIAL PRIMARY KEY,
                    department_name VARCHAR(100) NOT NULL
                )
            """)
            conn.commit()
            print("Table Created: departments.")
        except Exception as e:
            print("Error creating table: departments")
            print(e)
        finally:
            cursor.close()
            conn.close()

def create_table_teacher():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teacher (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL
                )
            """)
            conn.commit()
            print("Table Created: teacher.")
        except Exception as e:
            print("Error creating table: teacher")
            print(e)
        finally:
            cursor.close()
            conn.close()

def create_table_courses():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id SERIAL PRIMARY KEY,
                    course_name VARCHAR(100) NOT NULL,
                    department_id INT,
                    teacher_id INT REFERENCES teacher(id) ON DELETE SET NULL,
                    credits INT NOT NULL,
                    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
                )
            """)
            conn.commit()
            print("Table Created: courses.")
        except Exception as e:
            print("Error creating table: courses")
            print(e)
        finally:
            cursor.close()
            conn.close()

def create_table_students():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    enrollment_date DATE DEFAULT CURRENT_DATE
                )
            """)
            conn.commit()
            print("Table Created: students.")
        except Exception as e:
            print("Error creating table: students")
            print(e)
        finally:
            cursor.close()
            conn.close()

def create_table_enrollments():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enrollments (
                    enrollment_id SERIAL PRIMARY KEY,
                    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
                    course_id INT REFERENCES courses(course_id) ON DELETE CASCADE,
                    grade VARCHAR(2)
                )
            """)
            conn.commit()
            print("Table Created: enrollments.")
        except Exception as e:
            print("Error creating table: enrollments")
            print(e)
        finally:
            cursor.close()
            conn.close()
def insert_teacher(name, age):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO teacher (name, age) VALUES (%s, %s) RETURNING id", (name, age))
            conn.commit()
            print("Teacher Inserted.")
        except Exception as e:
            print("Error inserting teacher:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def insert_department(department_name):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO departments (department_name) VALUES (%s) RETURNING department_id", (department_name,))
            conn.commit()
            print("Department Inserted.")
        except Exception as e:
            print("Error inserting department:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def insert_course(course_name, department_id, credits, teacher_id=None):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO courses (course_name, department_id, credits, teacher_id) VALUES (%s, %s, %s, %s) RETURNING course_id", (course_name, department_id, credits, teacher_id))
            conn.commit()
            print("Course Inserted.")
        except Exception as e:
            print("Error inserting course:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def insert_student(first_name, last_name, email):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING student_id", (first_name, last_name, email))
            conn.commit()
            print("Student Inserted.")
        except Exception as e:
            print("Error inserting student:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def insert_enrollments(student_id, course_id, grade):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)", (student_id, course_id, grade))
            conn.commit()
            print("Student Enrolled in Course.")
        except Exception as e:
            print("Error enrolling student in course:")
            print(e)
        finally:
            cursor.close()
            conn.close()
def update_teacher(id, name=None, age=None):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if name:
                cursor.execute("UPDATE teacher SET name = %s WHERE id = %s", (name, id))
            if age:
                cursor.execute("UPDATE teacher SET age = %s WHERE id = %s", (age, id))
            conn.commit()
            print("Teacher Updated.")
        except Exception as e:
            print("Error updating teacher:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def update_department(department_id, department_name):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE departments SET department_name = %s WHERE department_id = %s", (department_name, department_id))
            conn.commit()
            print("Department Updated.")
        except Exception as e:
            print("Error updating department:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def update_course(course_id, course_name=None, department_id=None, credits=None, teacher_id=None):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if course_name:
                cursor.execute("UPDATE courses SET course_name = %s WHERE course_id = %s", (course_name, course_id))
            if department_id:
                cursor.execute("UPDATE courses SET department_id = %s WHERE course_id = %s", (department_id, course_id))
            if credits:
                cursor.execute("UPDATE courses SET credits = %s WHERE course_id = %s", (credits, course_id))
            if teacher_id:
                cursor.execute("UPDATE courses SET teacher_id = %s WHERE course_id = %s", (teacher_id, course_id))
            conn.commit()
            print("Course Updated.")
        except Exception as e:
            print("Error updating course:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def update_student(student_id, first_name=None, last_name=None, email=None):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if first_name:
                cursor.execute("UPDATE students SET first_name = %s WHERE student_id = %s", (first_name, student_id))
            if last_name:
                cursor.execute("UPDATE students SET last_name = %s WHERE student_id = %s", (last_name, student_id))
            if email:
                cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (email, student_id))
            conn.commit()
            print("Student Updated.")
        except Exception as e:
            print("Error updating student:")
            print(e)
        finally:
            cursor.close()
            conn.close()

def update_enrollment(enrollment_id, grade):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE enrollments SET grade = %s WHERE enrollment_id = %s", (grade, enrollment_id))
            conn.commit()
            print("Enrollment Updated.")
        except Exception as e:
            print("Error updating enrollment:")
            print(e)
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_table_departments()
    create_table_teacher()
    create_table_courses()
    create_table_students()
    create_table_enrollments()

    insert_department("Computer Science")
    insert_teacher("Bobby Joseph", 30)
    insert_course("Python", 1, 4, 1)  
    insert_student("Ram", "Thapa", "ramu@gmail.com")
    insert_enrollments(1, 1, "A")

    update_teacher(1, name="Bobby J.", age=31)
    update_department(1, "Information Technology")
    update_course(1, course_name="Advanced Python", credits=5)
    update_student(1, first_name="Jobby", last_name="Jacob", email="jobbyjacob@gmail.com")
    update_enrollment(1, grade="B")

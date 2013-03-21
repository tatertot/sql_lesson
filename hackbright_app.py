import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "add_project":
            joined_list = ' '.join(args)
            args = joined_list.split(',')
            add_project(*args)
        elif command == "grade":
            get_student_grade(*args)
        elif command == "add_grade":
            joined_list = ' '.join(args)
            args = joined_list.split(',')
            add_project(*args)
        elif command == "show_grades":
            show_grades(*args)

    CONN.close()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s"""%(row[0], row[1])

def add_project(title, description, max_grade):
    query = """INSERT INTO Projects VALUES (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s"%(title,description,max_grade)

def get_student_grade(github, title):
    query = """SELECT Students.first_name, Students.last_name,Grades.project_title, Grades.grade 
    FROM Students INNER JOIN Grades on Students.github = ? and Grades.project_title = ? """
    DB.execute(query, (github, title))
    row = DB.fetchone()
    print """\
Student: %s, %s, %s, %s"""%(row[0], row[1], row[2], row[3])

def give_grade(github):
    query = """INSERT INTO Grades VALUES (?,?,?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s %s %s"%(student_github,project_title,grade)

def show_grades(github):
    query = """SELECT Students.first_name, Students.last_name,Grades.project_title, Grades.grade 
    FROM Students INNER JOIN Grades on Students.github = ? """
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s, %s, %s, %s"""%(row[0], row[1], row[2], row[3])


    

if __name__ == "__main__":
    main()

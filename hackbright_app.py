import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row is None:
        print"""Student not in database."""
        main()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row is None:
        print "Project does not exist."
        main()
    print"""\
Project Title: %s 
Description: %s
Maximum Grade: %s"""%(row[0], row[1], row[2])

def get_grades_by_project(project):
    existing_query = """ SELECT title FROM Projects WHERE title = ?"""
    DB.execute(existing_query,(title,))
    existing_project = DB.fetchone()
    if existing_project is None:
        print "Project does not exist in database."
        main()
    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade 
    FROM Grades INNER JOIN Students ON Grades.student_github = Students.github WHERE Grades.project_title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchall()
    for i in range(len(row)):
        print"""\
Student: %s %s
Project: %s
Grade: %d"""%(row[i][0], row[i][1], row[i][2], row[i][3])

def get_student_grades(student_github):
    duplicate_query = """SELECT github FROM Students WHERE github = ?"""
    DB.execute(duplicate_query, (student_github,))
    duplicate_row = DB.fetchone()
    if duplicate_row is None:
        print"""Github account is not in database."""
        main()
    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade
    FROM Grades INNER JOIN Students ON Grades.student_github = Students.github WHERE Grades.student_github = ?"""
    DB.execute(query, (student_github,))
    row = DB.fetchall()
    print"""\
Student: %s %s"""%(row[0][0], row[0][1])
    for i in range(len(row)):
        print"""\
Project: %s
Grade: %d"""%(row[i][2], row[i][3])

def make_new_student(first_name, last_name, github):
    duplicate_query = """SELECT github FROM Students WHERE github = ?"""
    DB.execute(duplicate_query, (github,))
    git_account = DB.fetchone()
    if git_account != None:
        print "Github account already exists in database."
        main()
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name,last_name)

def make_new_project(title, description,max_grade):
    existing_query = """ SELECT title FROM Projects WHERE title = ?"""
    DB.execute(existing_query,(title,))
    existing_project = DB.fetchone()
    if existing_project != None:
        print "Project already exists."
        main()
    query = """INSERT into Projects values (?,?,?)"""
    number = int(max_grade)
    list_description = description.split('_')
    string_description = ' '.join(list_description)
    DB.execute(query,(title, string_description,number))
    CONN.commit()
    print "Successfully added a project: %s %s %d" % (title,string_description,number)

def make_new_grade(student_github,project_title,grade):
    #error-checking for duplicate grade in progress:
    #duplicate_query = """ SELECT grade FROM Grades WHERE github = ? AND project_title = ? """
    name_query = """SELECT Students.first_name,Students.last_name FROM Students WHERE github = ?"""
    DB.execute(name_query,(student_github,))
    student_name = DB.fetchone()
    query = """INSERT into Grades values (?,?,?)"""
    number_grade = int(grade)
    DB.execute(query,(student_github,project_title,number_grade))
    CONN.commit()
    print "Successfully added %s %s's grade for %s as %d" % (student_name[0], student_name[1],project_title,number_grade)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
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
            if args == []:
                print "Please enter a student's github account."
                main()
            get_student_by_github(*args) 
        elif command == "new_student":
            if len(args) < 3 or len(args) >= 4:
                print "Please enter a student's first and last name and their github account."
                main()
            make_new_student(*args)
        elif command == "project":
            if args == []:
                print "Please enter a project title."
                main()
            get_project_by_title(*args)
        elif command == "new_project":
            if args == []:
                print "Please enter a project title, description and maximum grade."
                main()
            make_new_project(*args)
        elif command == "get_project_grade":
            if args == []:
                print "Please enter a project's title."
                main()
            get_grades_by_project(*args)
        elif command == "make_new_grade":
            if args == []:
                print "Please enter a student's github account name, project title and their grade."
                main()
            make_new_grade(*args)
        elif command == "get_student_grades":
            if args == []:
                print "Please enter a student's github account."
                main()
            get_student_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()

"""All data structures needed for the Grade Hub and functions ptoject - SDG 4"""
faculty_data = {
    "FICT": {
        "programs": ["BSEM",
                     "BIT",
                     "BBIT",
                     "DIT",
                     "CIT"],
        "subjects": [
            "Structured Programming",
            "Database",
            "Software Engineering",
            "Communication Skills",
            "Computer Skills",
            "Computerized Maths",
            "French",
            "Mathematics",
            "Multimedia",
            "Data Communication"
        ]
    },
    "FCMB": {
        "programs": ["PC",
                     "BABJ",
                     "DMAB"],
        "subjects": [
            "Graphic Designing",
            "Digital Imaging",
            "Principles of Advertising",
            "Principles of Marketing",
            "Drawing"
        ]
    }
}

"""In-memory database to store users credentials and students grades"""
students = {} #stores key: students id, value: {password, name, faculty, program}
lecturers = {} #Stores key: username, value: {password}
grades = [] #Each element is a grade record (dictionary)


# Function 1: Calculate total grades(test, assignment, project, exam)
def calculate_total(test, assignment, project, exam):
    total = test * 0.20 + assignment * 0.15 + project * 0.30 + exam * 0.35
    total = round(total, 2)
    if total >= 90:
        grade = 'A+'
    elif total >= 80:
        grade = 'A'
    elif total >= 75:
        grade = 'B+'
    elif total >= 70:
        grade = 'B'
    elif total >= 65:
        grade = 'C+'
    elif total >= 60:
        grade = 'C'
    elif total >= 50:
        grade = 'C-'
    else:
        grade = 'F'

    return total, grade


# Function 2: Add or update new record
def add_grade(student_id, semester, faculty, module, test, assignment, project, exam):
    total, grade = calculate_total(test, assignment, project, exam)

    # Removes or overwrite old record with the same studentId/semester/faculty/module
    for i, g in enumerate(grades):
        if (g["student_id"] == student_id and g["semester"] == semester and
                g["faculty"] == faculty and g["module"] == module):
            grades.pop(i)
            break
    # Append the new grade (outside the loop)
    grades.append({
        'student_id': student_id,
        'semester': semester,
        "faculty": faculty,
        'module': module,
        'test': test,
        'assignment': assignment,
        'project': project,
        'exam': exam,
        'total': total,
        'grade': grade
    })


# Function 3: Get all grades for one student
def get_student_grades(student_id):
    result = []
    for g in grades:
        if g["student_id"] == student_id:
            result.append((
                g["semester"],
                g["faculty"],  # faculty first (matches dashboard column order)
                g["module"],
                g["test"],
                g["assignment"],
                g["project"],
                g["exam"],
                g["total"],
                g["grade"]
            ))
    return result


# Function 4: Student Login Validation
def student_login_validation(id_student, password):
    return id_student in students and students[id_student]['password'] == password


# Function 5: Lecturer Login Validation
def lecturer_login_validation(user, password):
    return user in lecturers and lecturers[user]['password'] == password


# Function 6: Register a new student
def register_student(id_student, password, name, faculty, program):
    if id_student in students:
        return False
    # This save the student's name, faculty, program, and password of a user in Students dictionary
    students[id_student] = {
        'name': name,
        'faculty': faculty,
        'program': program,
        'password': password
    }
    return True


# Function 7: Register a new lecturer
def register_lecturer(user, password):
    if user in lecturers:
        return False
    # This save the username and password of a user in lecturers dictionary
    lecturers[user] = {"password": password}
    return True
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


# Function 2: Add or update grade record
def add_grade(student_id, semester, module, test, assignment, project, exam):
    total, grade = calculate_total(test, assignment, project, exam)
    # Enumerate create and return a new object
    for i, g in enumerate(grades):
        # Removes grade with the same semester/module/studentId
        if g['student_id'] == student_id and g['semester'] == semester and g['module'] == module:
            grades.pop(i)
            break
        grades.append({
            'student_id': student_id,
            'semester': semester,
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

    result = [] #Empty list for result that will store all grades for one student
    for g in grades:
        if g['student_id'] == student_id:
            result.append((
                g['semester'],
                g['mopdule'],
                g['test'],
                g['assignment'],
                g['project'],
                g['exam'],
                g['total'],
                g['grade']
            ))
        return result

# Function 4: Student Login Validation
def student_login_validation(student_id, password):
    return student_id in students and students['student_id']['password'] == password

# Function 5: Lecturer Login Validation
def lecturer_login_validation(username, password):
    return username in lecturers and lecturers[username]['password'] == password

# Function 6: Register a new student
def register_student(student_id, password, name, faculty, program):
    if student_id in students:
        return False
    # This is an else statement
    students[studnet_id] = {
        'name': name,
        'faculty': faculty,
        'program': program,
        'password': password
    }
    return True

# Function 7: Register a new lecturer
def register_lecturer(username, password)
    if username in lecturers:
        return False
    # This is an else statement
    lecturers[username] = {password}
    return True
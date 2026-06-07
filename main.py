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

# Function 4:

# Function 5:

# Function 6:

# Function 7:
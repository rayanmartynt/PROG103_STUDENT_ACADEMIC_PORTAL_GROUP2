# tkinter provides GUI components: windows, buttons, labels, text boxes, etc.
import tkinter as tk

# messagebox shows pop-up alerts like errors, success messages, and warnings
from tkinter import messagebox

# ttk gives modern theme widgets like combo boxes (dropdown menus) and modern treeviews (tables)
import ttkbootstrap as ttk


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
    students[student_id] = {
        'name': name,
        'faculty': faculty,
        'program': program,
        'password': password
    }
    return True

# Function 7: Register a new lecturer
def register_lecturer(username, password):
    if username in lecturers:
        return False
    # This is an else statement
    lecturers[username] = {password}
    return True

# Function 8: Display Lecturer Dashboard
def lecturer_dashboard(parent, username):
    win = ttk.Toplevel(parent)
    win.title(f'Lecturer Dashboard - {username}')
    win.geometry('850x550')

    ttk.Label(master = win,
             text = 'Upload Student Grade').pack(pady = 5)

    # Input frame
    frame = ttk.Frame(master = win)
    frame.pack(pady = 10)

    # Semester
    ttk.Label(master = frame,
             text = 'Semester').grid(row = 0,
                                     column = 0,
                                     pady = 5,
                                     padx = 5,
                                     sticky = 'e')
    semester_var = tk.StringVar(value = 'Semester 1')
    sem_combo = ttk.Combobox(master = frame,
                             textvariable = semester_var,
                             state = 'readonly',
                             values = [f'Semester {i}' for i in range(1, 7)],
                             width = 12)
    sem_combo.grid(row = 0,
                   column = 1,
                   padx = 5)

    # Student ID
    ttk.Label(master = frame,
             text = 'Student ID:').grid(row = 1,
                                        column = 0,
                                        pady = 5,
                                        padx = 5,
                                        sticky = 'e')
    studentID_entry = ttk.Entry(master = frame,
                                width = 15)
    studentID_entry.grid(column = 1,
                         row = 1,
                         padx = 5)

    # Marks
    ttk.Label(master = frame,
              text = 'Test (20%):').grid(row = 2,
                                         column = 0,
                                         pady = 5,
                                         padx = 5,
                                         sticky = 'e')
    test_entry = ttk.Entry(master = frame,
                           width = 10)
    test_entry.grid(row = 2,
                    column = 1)

    ttk.Label(master = frame,
              text = 'Assignment (15%):').grid(row = 2,
                                               column = 2,
                                               padx = 5,
                                               pady = 5,
                                               sticky = 'e')
    assignment_entry = ttk.Entry(master = frame,
                                 width = 10)
    assignment_entry.grid(row = 2,
                          column = 3)

    ttk.Label(master = frame,
              text = 'Project (30%):').grid(row = 3,
                                            column = 0,
                                            padx = 5,
                                            pady = 5,
                                            sticky = 'e')
    project_entry = ttk.Entry(master = frame,
                              width = 10)
    project_entry.grid(row = 3,
                       column = 1)

    ttk.Label(master = frame,
              text = 'Exam (35%):').grid(row = 3,
                                         column = 2,
                                         padx = 5,
                                         pady = 5,
                                         sticky = 'e')
    exam_entry = ttk.Entry(master = frame,
                           width = 10)
    exam_entry.grid(row = 3,
                    column = 3)

    # Grade preview
    preview_label = ttk.Label(master = win,
                              text = 'Total: ---  Grade: ---')
    preview_label.pack(pady = 5)

    # Grade table (all grades)
    ttk.Label(master = win,
              text = 'All Grades in System').pack(pady = 5)
    cols2 = ('Student ID', 'Semester', 'Subject', 'Test', 'Assignment', 'Project', 'Exam', 'Total', 'Grade')

    tree_all = ttk.Treeview(master = win,
                            columns = cols2,
                            show = 'headings',
                            height = 8)
    for col in cols2:
        tree_all.heading(col,
                         text = col)
        tree_all.column(col,
                        width = 70,
                        anchor = 'center')
    tree_all.column("Subject",
                    width = 120)
    tree_all.pack(fill = tk.BOTH,
                  expand = True,
                  padx = 10,
                  pady = 5)

    def refresh_all_grades():
        for row in tree_all.get_children():
            tree_all.delete(row)
        for g  in grades:
            tree_all.insert("",
                            "end",
                            values = (g['student_id'],
                                      g['semester'],
                                      g['subject'],
                                      g['test'],
                                      g['assignment'],
                                      g['project'],
                                      g['exam'],
                                      g['total'],
                                      g['grade']))

    def preview():




def main():
    root = ttk.Window(themename = 'cyborg')
    root.title("Limkokwing Student Academic Portal")
    root.geometry('500x500')

    root.mainloop()

if __name__ == '__main__':
    main()
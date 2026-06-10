# tkinter provides GUI components: windows, buttons, labels, text boxes, etc.
import tkinter as tk

# messagebox shows pop-up alerts like errors, success messages, and warnings
from tkinter import messagebox

# ttk gives modern theme widgets like combo boxes (dropdown menus) and modern tree views (tables)
import ttkbootstrap as ttk

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
    

# Function 3: Get all grades for one student
def get_student_grades(student_id):

    result = [] #Empty list for result that will store all grades for one student
    for g in grades:
        if g["student_id"] == student_id:
            result.append((
                g["semester"],
                g["faculty"],
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
    lecturers[user] = {"password":password}
    return True

# Function 8: Display Student Dashboard
def student_dashboard(parent, student_id):
    win = ttk.Toplevel(master = parent)
    win.title(f'Student Dashboard - {student_id}')
    win.geometry('750x400')

    student = students[student_id]
    ttk.Label(master = win,
              text = f'Welcome {student['name']} ({student['program']})',
              font = 14).pack(pady = 10)

    # Treeview to show all grades with columns
    columns = ('Semester',
               'Faculty',
               'Module',
               'Test(20%)',
               'Assignment(15%)',
               'Project(30%)',
               'Exam(35%)',
               'Total',
               'Grade')
    tree = ttk.Treeview(master = win,
                        columns = columns,
                        show = 'headings')
    for col in columns:
        tree.heading(col, text = col)
        tree.column(col,
                    width = 85,
                    anchor = 'center')
    tree.column('Module',
                width = 130)
    tree.column('Faculty',
                width=120)
    tree.pack(fill = tk.BOTH,
              expand = True,
              padx = 10,
              pady = 5)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        grade_list = get_student_grades(student_id)
        if not grade_list:
            tree.insert("", "end", values = ("No grades uploaded yet", "", "", "", "", "", "", ""))
        else:
            for g in grade_list:
                tree.insert("", "end", values = g)
    refresh()

    # Buttons
    ttk.Button(master = win,
               text = 'Refresh',
               command = refresh).pack(pady = 10)

    ttk.Button(master = win,
               text = 'Logout',
               command = win.destroy).pack(pady = 5)

# Function 9: Display Lecturer Dashboard
def lecturer_dashboard(parent, username):
    win = ttk.Toplevel(parent)
    win.title(f'Lecturer Dashboard - {username}')
    win.geometry('850x550')

    ttk.Label(master = win,
             text = 'Upload Student Grade',
              font = ("", 14)).pack(pady = 5)

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
    semester_var = ttk.StringVar(value = 'Semester 1')
    sem_combo = ttk.Combobox(master = frame,
                             textvariable = semester_var,
                             state = 'readonly',
                             values = [f'Semester {i}' for i in range(1, 7)],
                             width = 12)
    sem_combo.grid(row = 0,
                   column = 1,
                   padx = 5)

    # Faculty
    ttk.Label(master = frame,
              text='Faculty:').grid(row = 0,
                                    column = 2,
                                    padx = 5,
                                    pady = 5,
                                    sticky = 'e')
    faculty_var = ttk.StringVar(value = list(faculty_data.keys())[0])
    faculty_combo = ttk.Combobox(master = frame,
                                 textvariable = faculty_var,
                                 state = 'readonly',
                                 values = list(faculty_data.keys()),
                                 width=20)
    faculty_combo.grid(row = 0,
                       column = 3,
                       padx = 5)

    # Module (subject) - updates when faculty changes
    ttk.Label(master = frame,
              text='Module:').grid(row = 1,
                                   column = 0,
                                   padx = 5,
                                   pady = 5,
                                   sticky = 'e')
    module_var = ttk.StringVar()
    module_combo = ttk.Combobox(master = frame,
                                textvariable = module_var,
                                state = 'readonly',
                                width = 20)

    def update_module(*args):
        faculty = faculty_var.get()
        subjects = faculty_data.get(faculty, {}).get("subjects", [])
        module_combo['values'] = subjects
        if subjects:
            module_var.set(subjects[0])

    faculty_combo.bind('<<ComboboxSelected>>',
                       update_module)
    update_module()  # initial load
    module_combo.grid(row = 1,
                      column = 1,
                      columnspan = 3,
                      padx = 5,
                      pady = 5,
                      sticky = 'w')

    # Student ID
    ttk.Label(master = frame,
             text = 'Student ID:').grid(row = 1,
                                        column = 2,
                                        pady = 5,
                                        padx = 5,
                                        sticky = 'e')
    studentID_entry = ttk.Entry(master = frame,
                                width = 15)
    studentID_entry.grid(row = 1,
                         column = 3,
                         padx = 5)

    # Marks
    ttk.Label(master = frame,
              text = 'Test (20%):').grid(row = 3,
                                         column = 0,
                                         pady = 5,
                                         padx = 5,
                                         sticky = 'e')
    test_entry = ttk.Entry(master = frame,
                           width = 10)
    test_entry.grid(row = 3,
                    column = 1)

    ttk.Label(master = frame,
              text = 'Assignment (15%):').grid(row = 3,
                                               column = 2,
                                               padx = 5,
                                               pady = 5,
                                               sticky = 'e')
    assignment_entry = ttk.Entry(master = frame,
                                 width = 10)
    assignment_entry.grid(row = 3,
                          column = 3)

    ttk.Label(master = frame,
              text = 'Project (30%):').grid(row = 4,
                                            column = 0,
                                            padx = 5,
                                            pady = 5,
                                            sticky = 'e')
    project_entry = ttk.Entry(master = frame,
                              width = 10)
    project_entry.grid(row = 4,
                       column = 1)

    ttk.Label(master = frame,
              text = 'Exam (35%):').grid(row = 4,
                                         column = 2,
                                         padx = 5,
                                         pady = 5,
                                         sticky = 'e')
    exam_entry = ttk.Entry(master = frame,
                           width = 10)
    exam_entry.grid(row = 4,
                    column = 3)

    # Grade preview
    preview_label = ttk.Label(master = win,
                              text = 'Total: ---  Grade: ---',
                              font = 11)
    preview_label.pack(pady = 5)

    # Grade table (all grades)
    ttk.Label(master = win,
              text = 'All Grades in System',
              font = 12).pack(pady = 5)
    cols2 = ('Student ID', 'Semester', 'Faculty', 'Module', 'Test (20%)', 'Assignment (15%)', 'Project (30%)', 'Exam (35%)', 'Total', 'Grade')

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
    tree_all.column("Module",
                    width = 120)
    tree_all.column('Faculty',
                    width=120)
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
                                      g['faculty'],
                                      g['module'],
                                      g['test'],
                                      g['assignment'],
                                      g['project'],
                                      g['exam'],
                                      g['total'],
                                      g['grade']))

    def preview():
        try:
            test = float(test_entry.get())
            assignment = float(assignment_entry.get())
            project = float(project_entry.get())
            exam = float(exam_entry.get())
            total, grade = calculate_total(test, assignment, project, exam)
            preview_label.config(text = f'Total: {total} Grade: {grade}')
        except ValueError:
            preview_label.config(text = 'Enter valid numbers 0-100')

    def save():
        id_student = studentID_entry.get().strip() #Using strip function to remove whitespaces
        if id_student not in students:
            messagebox.showerror('Error',f'Student ID: {id_student} does not exist. This student needs to register first.')

        try:
            test = float(test_entry.get())
            assignment = float(assignment_entry.get())
            project = float(project_entry.get())
            exam = float(exam_entry.get())

            # Display error message if any grade is less than 0 or greater than 100
            if not (0 <= test <= 100 and
                    0 <= assignment <= 100 and
                    0 <= project <= 100 and
                    0 <= exam <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'Enter valid numbers 0-100 for all grades.')
            return

        add_grade(id_student,
                  semester_var.get(),
                  faculty_var.get(),
                  module_var.get(),
                  test,
                  assignment,
                  project,
                  exam)
        messagebox.showinfo('Success',f'Grade saved for {id_student}')
        refresh_all_grades()

        # Clear Entries
        studentID_entry.delete(0, tk.END)
        test_entry.delete(0, tk.END)
        assignment_entry.delete(0, tk.END)
        project_entry.delete(0, tk.END)
        exam_entry.delete(0, tk.END)
        preview_label.config(text = 'Total: ---  Grade: ---')

    # Buttons
    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady = 10)

    # Preview button
    ttk.Button(master = btn_frame,
                text = 'Preview Grade',
                command = preview).pack(side = 'left',
                                        padx = 5)
    # Save Grade button
    ttk.Button(master = btn_frame,
                text = 'Save Grade',
                command = save).pack(side = 'left',
                                    padx = 5)

    # Refresh button
    ttk.Button(master = btn_frame,
                text = 'Refresh Grades',
                command = refresh_all_grades).pack(side = 'left',
                                                    padx = 5)
    # Logout button
    ttk.Button(master = btn_frame,
                text = 'Logout',
                command = win.destroy).pack(side = 'left',
                                            padx = 5)
    refresh_all_grades()

def main():
    root = ttk.Window(themename = 'vapor')
    root.title("Grade Hub - (SDG4)")
    root.geometry('500x500')

    # Notebook (Tabs)
    tab = ttk.Notebook(root)
    tab.pack(fill = 'both',
             expand = True,
             padx = 10,
             pady = 10)

    # ---- LOGIN TAB ----
    login_tab = ttk.Frame(master = tab)
    tab.add(login_tab,
            text = 'Login')

    # Role dropdown
    ttk.Label(master = login_tab,
              text = 'Role:').grid(row = 0,
                                   column = 0,
                                   sticky = 'e',
                                   padx = 10,
                                   pady = 10)
    role_var = ttk.StringVar(value = "Student")
    role_combo = ttk.Combobox(master = login_tab,
                              textvariable = role_var,
                              values = ["Student", "Lecturer"],
                              state = 'readonly',
                              width = 12)
    role_combo.grid(row = 0,
                    column = 1,
                    sticky = 'w',
                    padx = 10,
                    pady = 10)

    # Username/ID entry field
    tk.Label(master = login_tab,
             text="ID / Username:").grid(row = 1,
                                         column = 0,
                                         pady = 10,
                                         padx = 10,
                                         sticky = " e")
    login_user = tk.Entry(master = login_tab,
                          width=20)
    login_user.grid(row=1,
                    column=1,
                    pady=10,
                    padx=10)

    # Password Entry field
    tk.Label(master = login_tab,
             text="Password:",).grid(row=2,
                                     column=0,
                                     pady=10,
                                     padx=10,
                                     sticky="e")
    login_pwd = tk.Entry(master = login_tab,
                         show="*",
                         width=20)
    login_pwd.grid(row=2,
                   column=1,
                   pady=10,
                   padx=10)

    def do_login():
        role = role_var.get()
        username_id = login_user.get().strip()
        password = login_pwd.get()
        if not username_id or not password:
            messagebox.showerror("Error", "Please fill both fields")
            return
        if role == "Student":
            if student_login_validation(username_id, password):
                student_dashboard(root, username_id)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid Student ID or Password")
        else:  # Lecturer
            if lecturer_login_validation(username_id, password):
                lecturer_dashboard(root, username_id)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid Lecturer credentials")

    tk.Button(login_tab,
              text="Login",
              command=do_login,
              width=15).grid(row = 3,
                             column = 0,
                             columnspan = 2,
                             pady = 20)

    # ----- STUDENT SIGNUP TAB -----
    student_tab = ttk.Frame(master = tab)
    tab.add(student_tab,
            text="Student Signup")

    tk.Label(student_tab,
             text="Student ID:").grid(row=0,
                                      column=0,
                                      pady=5,
                                      padx=10,
                                      sticky="e")
    id_for_student = tk.Entry(master = student_tab)
    id_for_student.grid(row=0,
               column=1,
               pady=5)

    tk.Label(master = student_tab,
             text="Full Name:").grid(row=1,
                                     column=0,
                                     pady=5,
                                     padx=10,
                                     sticky="e")
    student_name = tk.Entry(master = student_tab)
    student_name.grid(row=1,
                      column=1,
                      pady=5)

    tk.Label(master = student_tab,
             text="Password:").grid(row=2,
                                    column=0,
                                    pady=5,
                                    padx=10,
                                    sticky="e")
    s_password = tk.Entry(master = student_tab,
                     show="*")
    s_password.grid(row=2,
               column=1,
               pady=5)

    tk.Label(master = student_tab,
             text="Confirm Password:").grid(row=3,
                                            column=0,
                                            pady=5,
                                            padx=10,
                                            sticky="e")
    studentConfirm_password = tk.Entry(master = student_tab,
                                       show="*")
    studentConfirm_password.grid(row=3,
                                 column=1,
                                 pady=5)

    tk.Label(master = student_tab, text="Faculty:"
             ).grid(row=4,
                    column=0,
                    pady=5,
                    padx=10,
                    sticky="e")
    faculty_var = ttk.StringVar(value=list(faculty_data.keys())[0])
    faculty_signup_combo = ttk.Combobox(student_tab, textvariable=faculty_var,
                                        values=list(faculty_data.keys()), state='readonly', width=25)
    faculty_signup_combo.grid(row=4, column=1, padx=10, pady=5)

    ttk.Label(student_tab, text='Program:').grid(row=5, column=0, padx=10, pady=5, sticky='e')
    program_signup_var = ttk.StringVar()
    program_combo = ttk.Combobox(student_tab, textvariable=program_signup_var, state='readonly', width=25)

    def update_programs(*args):
        faculty = faculty_var.get()
        program = faculty_data.get(faculty, {}).get('programs', [])
        program_combo['values'] = program
        if program:
            program_signup_var.set(program[0])
    faculty_signup_combo.bind('<<ComboboxSelected>>',
                              update_programs)
    update_programs()
    program_combo.grid(row=5, column=1, padx=10, pady=5)

    def do_student_signup():
        id_student = id_for_student.get().strip()
        name = student_name.get().strip()
        password = s_password.get()
        confirm_password = studentConfirm_password.get()
        faculty = faculty_var.get()
        program = program_combo.get()
        if not id_student or not name or not password:
            messagebox.showerror("Error", "ID, Name and Password required")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if register_student(id_student, password, name, faculty, program):
            messagebox.showinfo("Success", f"Student {id_student} registered! You can now log in.")
            id_for_student.delete(0, tk.END)
            student_name.delete(0, tk.END)
            s_password.delete(0, tk.END)
            studentConfirm_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Student ID {id_student} already exists")

    tk.Button(master = student_tab,
              text="Register Student",
              command=do_student_signup,
              width=18).grid(row=6,
                             column=0,
                             columnspan=2,
                             pady=15)

    # ----- LECTURER SIGNUP TAB -----
    lecturer_tab = tk.Frame(master = tab)
    tab.add(lecturer_tab,
            text="Lecturer Signup")

    tk.Label(master = lecturer_tab,
             text="Username:").grid(row=0,
                                    column=0,
                                    pady=10,
                                    padx=10,
                                    sticky="e")
    lecturer_username = tk.Entry(master = lecturer_tab)
    lecturer_username.grid(row=0,
                column=1,
                pady=10)

    tk.Label(master = lecturer_tab,
             text="Password:").grid(row=1,
                                    column=0,
                                    pady=10,
                                    padx=10,
                                    sticky="e")
    lecturer_password = tk.Entry(master = lecturer_tab,
                                 show="*")
    lecturer_password.grid(row=1,
                           column=1,
                           pady=10)

    tk.Label(master = lecturer_tab,
             text="Confirm Password:").grid(row=2,
                                            column=0,
                                            pady=10,
                                            padx=10,
                                            sticky="e")
    lecturerConfirm_password = tk.Entry(master = lecturer_tab,
                                        show="*")
    lecturerConfirm_password.grid(row=2,
                                  column=1,
                                  pady=10)

    def do_lecturer_signup():
        user = lecturer_username.get().strip()
        password = lecturer_password.get()
        confirm_password = lecturerConfirm_password.get()
        if not user or not password:
            messagebox.showerror("Error", "Username and password required")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if register_lecturer(user, password):
            messagebox.showinfo("Success", f"Lecturer {user} registered! You can now log in.")
            lecturer_username.delete(0, tk.END)
            lecturer_password.delete(0, tk.END)
            lecturerConfirm_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Username {user} already taken")

    tk.Button(master = lecturer_tab,
              text="Register Lecturer",
              command=do_lecturer_signup,
              width=18).grid(row=3,
                             column=0,
                             columnspan=2,
                             pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()

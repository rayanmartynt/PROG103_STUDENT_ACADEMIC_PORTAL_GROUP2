# tkinter provides GUI components: windows, buttons, labels, text boxes, etc.
import tkinter as tk
from email.policy import default

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

# Function 8: Display Student Dashboard
def student_dashboard(parent, student_id):
    win = ttk.Toplevel(master = parent)
    win.title(f'Student Dashboard - {student_id}')
    win.geometry('750x400')

    student = students[student_id]
    ttk.Label(master = win,
              text = f'Welcome {student['name']} ({student['program']})', font = ('Arial', 14)).pack(pady = 10)

    # Treeview to show all grades with columns
    columns = ['Semester', 'Subject', 'Test(20%)', 'Assign(15%)', 'Project(30%)', 'Exam(35%)', 'Total', 'Grade']
    tree = ttk.Treeview(master = win,
                        columns = columns,
                        show = 'headings')
    tree.pack(fill = tk.BOTH,
              expand = True,
              padx = 10,
              pady = 5)

    def refresh():
        for row in tree.get_children(student_id):
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
               command = win.destroy).pack(pady = 10)

# Function 9: Display Lecturer Dashboard
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

    # Subject
    module = ['Structured Programming',
              'Database',
              'Software Engineering',
              'Communication Skills',
              'Computer Skills',
              'Computerized Maths',
              'French',
              'Mathematics',
              'Multimedia',
              'Data Communication']
    ttk.Label(master = frame,
              text = 'Module').grid(row = 1,
                                    column = 0,
                                    pady = 5,
                                    padx = 5,
                                    sticky = 'e')
    module_var = tk.StringVar(value = module[0])
    module_combo = ttk.Combobox(master = frame,
                                textvariable = module_var,
                                state = 'readonly',
                                width = 15)
    module_combo.grid(column = 3,
                      row = 0,
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
        try:
            test = float(test_entry.get())
            assignment = float(assignment_entry.get())
            project = float(project_entry.get())
            exam = float(exam_entry.get())
            total, grade = calculate_total(test, assignment, project, exam)
            preview_label.config(text = f'Total: {total} Grade: {grade}')
        except:
            preview_label.config(text = 'Enter valid numbers 0-100')

    def save():
        student_id = studentID_entry.get().strip() #Using strip function to remove whitespaces
        if student_id not in students:
            messagebox.showerror(f'Student ID: {student_id} does not exist. This student needs to register first.')

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
        except:
            messagebox.showerror('Error', 'Enter valid numbers 0-100 for all grades.')
            return

        add_grade(student_id, semester_var.get(), module_var.get(), test, assignment, project, exam)
        messagebox.showinfo('Success',f'Grade saved for {student_id}')
        refresh_all_grades()

        # Clear Entries
        studentID_entry.delete(0, 'end')
        test_entry.delete(0, 'end')
        assignment_entry.delete(0, 'end')
        project_entry.delete(0, 'end')
        exam_entry.delete(0, 'end')
        preview_label.config(text = 'Total: ---  Grade: ---')

        # Buttons
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady = 5)

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
    root = ttk.Window(themename = 'cyborg')
    root.title("Limkokwing Student Academic Portal")
    root.geometry('500x500')

    # Tabs
    tab = ttk.Notebook(root)
    tab.pack(fill = 'both',
             expand = True,
             padx = 10,
             pady = 10)

    # ---- LOGIN TAB ----
    login_tab = ttk.Frame(tab)
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
    tk.Label(login_tab,
             text="ID / Username:").grid(row = 1,
                                         column = 0,
                                         pady = 10,
                                         padx = 10,
                                         sticky = " e")
    login_user = tk.Entry(login_tab,
                          width=20)
    login_user.grid(row=1,
                    column=1,
                    pady=10,
                    padx=10)

    # Password Entry field
    tk.Label(login_tab,
             text="Password:",).grid(row=2,
                                     column=0,
                                     pady=10,
                                     padx=10,
                                     sticky="e")
    login_pwd = tk.Entry(login_tab,
                         show="*",
                         width=20)
    login_pwd.grid(row=2,
                   column=1,
                   pady=10,
                   padx=10)

    def do_login():
        role = role_var.get()
        id_username = login_user.get().strip()
        password = login_pwd.get()
        if not id_username or not password:
            messagebox.showerror("Error", "Please fill both fields")
            return
        if role == "Student":
            if student_login_validation(id_username, password):
                student_dashboard(root, id_username)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid Student ID or Password")
        else:  # Lecturer
            if lecturer_login_validation(id_username, password):
                lecturer_dashboard(root, id_username)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid Lecturer credentials")


    tk.Button(login_tab,
              text="Login",
              command=do_login,
              width=15).grid(row=3,
                             column=0,
                             columnspan=2,
                             pady=20)

    # ----- STUDENT SIGNUP TAB -----
    student_tab = tk.Frame(tab)
    tab.add(student_tab,
            text="Student Signup")

    tk.Label(student_tab,
             text="Student ID:").grid(row=0,
                                                   column=0,
                                                   pady=5,
                                                   padx=10,
                                                   sticky="e")
    student_id = tk.Entry(student_tab)
    student_id.grid(row=0,
               column=1,
               pady=5)

    tk.Label(student_tab,
             text="Full Name:").grid(row=1,
                                                  column=0,
                                                  pady=5,
                                                  padx=10,
                                                  sticky="e")
    student_name = tk.Entry(student_tab)
    student_name.grid(row=1,
                column=1,
                pady=5)

    tk.Label(student_tab,
             text="Password:").grid(row=2,
                                    column=0,
                                    pady=5,
                                    padx=10,
                                    sticky="e")
    s_pwd = tk.Entry(student_tab,
                     show="*")
    s_pwd.grid(row=2,
               column=1,
               pady=5)

    tk.Label(student_tab,
             text="Confirm Password:").grid(row=3,
                                                         column=0,
                                                         pady=5,
                                                         padx=10,
                                                         sticky="e")
    studentConfirm_password = tk.Entry(student_tab,
                                       show="*")
    studentConfirm_password.grid(row=3,
                                 column=1,
                                 pady=5)

    tk.Label(student_tab, text="Faculty:"
             ).grid(row=4,
                    column=0,
                    pady=5,
                    padx=10,
                    sticky="e")
    faculty_entry = tk.Entry(master = student_tab)
    faculty_entry.insert("Faculty of ICT")
    faculty_entry.config(state="readonly")
    faculty_entry.grid(row=4, column=1, pady=5)

    tk.Label(student_tab, text="Program:").grid(row=5,
                                                column=0,
                                                pady=5,
                                                padx=10,
                                                sticky="e")
    programs = ["BSEM", "BIT", "BBIT", "DIT", "CIT"]
    program_combo = ttk.Combobox(student_tab,
                              values=programs,
                              state="readonly",
                              width=17)
    program_combo.current(0)
    program_combo.grid(row=5,
                    column=1,
                    pady=5)

    def do_student_signup():
        studentId = student_id.get().strip()
        studentName = student_name.get().strip()
        s_password = password.get()
        confirm_password = studentConfirm_password.get()
        faculty = faculty_entry.get()
        program = program_combo.get()
        if not studentId or not studentName or not s_password:
            messagebox.showerror("Error", "ID, Name and Password required")
            return
        if s_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if register_student(student_id, s_password, studentName, faculty, program):
            messagebox.showinfo("Success", f"Student {studentId} registered! You can now log in.")
            student_id.delete(0, tk.END)
            student_name.delete(0, tk.END)
            s_password.delete(0, tk.END)
            confirm_password.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Student ID {studentId} already exists")

    tk.Button(student_tab, text="Register Student",
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

    tk.Label(master = lecturer_tab, text="Password:").grid(row=1,
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
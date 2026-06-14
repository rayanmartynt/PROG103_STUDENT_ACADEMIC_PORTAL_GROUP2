import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

#Import all the functions and data structures from logic
from logic import *

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
               bootstyle="primary",
               command = refresh).pack(pady = 10)

    ttk.Button(master = win,
               text = 'Logout',
               bootstyle="danger",
               command = win.destroy).pack(pady = 5)

# Function 9: Display Lecturer Dashboard
def lecturer_dashboard(parent, username):
    win = ttk.Toplevel(parent)
    win.title(f'Lecturer Dashboard - {username}')
    win.geometry('950x650')

    ttk.Label(master = win,
             text = 'Upload Student Grade',
              font = ("", 14)).pack(pady = 5)

    # Input frame
    frame = ttk.Frame(master = win)
    frame.pack(pady = 10)

    # Semester
    ttk.Label(master = frame,
             text = 'Semester:').grid(row = 0,
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

    # Program
    ttk.Label(master = frame,
              text='Program:').grid(row = 1,
                                    column = 0,
                                    padx = 5,
                                    pady = 5,
                                    sticky = 'e')
    program_var = ttk.StringVar(value = list(faculty_data.keys())[0])
    program_combo = ttk.Combobox(master = frame,
                                 textvariable = program_var,
                                 state = 'readonly',
                                 values = list(faculty_data.keys()),
                                 width=20)
    program_combo.grid(row = 1,
                       column = 1,
                       padx = 5)

    # Module (subject) - updates when faculty changes
    ttk.Label(master = frame,
              text='Module:').grid(row = 1,
                                   column = 2,
                                   padx = 5,
                                   pady = 5,
                                   sticky = 'e')
    module_var = ttk.StringVar()
    module_combo = ttk.Combobox(master = frame,
                                textvariable = module_var,
                                state = 'readonly',
                                width = 20)

    # The args allows the function to accept any number of positional arguments, packing them into a tuple(collection of values)
    def lecturer_update_programs(*args):
        faculty = faculty_var.get()

        programs = list(faculty_data.get(faculty, {}).get('programs', {}).keys())

        program_combo['values'] = programs
        if programs:
            program_var.set(programs[0])
            update_module()

    # This function allows the lecturer to update student module
    # The args allows the function to accept any number of positional arguments, packing them into a tuple(collection of values)
    def update_module(*args):
        faculty = faculty_var.get()
        program = program_var.get()
        semester = semester_var.get()

        subjects = faculty_data.get(faculty, {}).get('programs', {}).get(program, {}).get(semester, {}).get('subjects', [])
        # try:
        #     subjects = faculty_data[faculty]['programs'][program][semester]['subjects']
        # except KeyError:
        #     subjects = []
        module_combo['values'] = subjects
        if subjects:
            module_var.set(subjects[0])
        else:
            module_var.set('')
    faculty_combo.bind('<<ComboboxSelected>>',
                       lecturer_update_programs)

    program_combo.bind('<<ComboboxSelected>>',
                       update_module)

    sem_combo.bind('<<ComboboxSelected>>',
                   update_module)
    lecturer_update_programs()  # initial load
    module_combo.grid(row = 1,
                      column = 3,
                      columnspan = 5,
                      padx = 5,
                      pady = 5,
                      sticky = 'e')

    # Student ID
    ttk.Label(master = frame,
             text = 'Student ID:').grid(row = 2,
                                        column = 0,
                                        pady = 5,
                                        padx = 5,
                                        sticky = 'e')
    studentID_entry = ttk.Entry(master = frame,
                                width = 15)
    studentID_entry.grid(row = 2,
                         column = 1,
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

        if id_student == "":
             preview_label.config(text = 'Student ID must not be empty.')
             return

        if id_student not in students:
            preview_label.config(text = f'Student ID: {id_student} does not exist. This student needs to register first.')
            return


        # Get students faculty and the program they are in
        selected_program = program_var.get()
        selected_faculty = faculty_var.get()

        # Checks if the student is in the faculty and the correct program, if not, an error message will appear
        student_faculty = students[id_student]['faculty']
        student_program = students[id_student]['program']

        if student_program != selected_program or student_faculty != selected_faculty:
            preview_label.config(text = f'Student ID: {id_student} belongs to' " " f'{student_faculty} - {student_program}')
            return
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
            preview_label.config(text = 'Enter valid numbers 0-100 for all grades.')
            return

        add_grade(id_student,
                  semester_var.get(),
                  faculty_var.get(),
                  module_var.get(),
                  test,
                  assignment,
                  project,
                  exam)
        preview_label.config(text = f'Grade saved for {id_student}')
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
                bootstyle="success",
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
               bootstyle="danger",
               command = win.destroy).pack(side = 'left',
                                            padx = 5)
    refresh_all_grades()

def main():
    root = ttk.Window(themename = 'sandstone')
    root.title("Grade Hub - (SDG4)")
    root.geometry('500x500')

    # Notebook (Tabs)
    tab = ttk.Notebook(root)
    tab.pack(expand = True,
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
    ttk.Label(master = login_tab,
             text="ID / Username:").grid(row = 1,
                                         column = 0,
                                         pady = 10,
                                         padx = 10,
                                         sticky = " e")
    login_user = ttk.Entry(master = login_tab,
                          width=20)
    login_user.grid(row=1,
                    column=1,
                    pady=10,
                    padx=10)

    # Password Entry field
    ttk.Label(master = login_tab,
             text="Password:",).grid(row = 2,
                                     column = 0,
                                     pady = 10,
                                     padx = 10,
                                     sticky = "e")
    login_pwd = ttk.Entry(master = login_tab,
                         show = "*",
                         width = 20)
    login_pwd.grid(row = 2,
                   column = 1,
                   pady = 10,
                   padx = 10)

    login_status = ttk.Label(master = login_tab,
                             text = "",
                             foreground = "red")
    login_status.grid(row = 3,
                      column = 0,
                      columnspan = 2,
                      pady = 5)

    def do_login():
        login_status.config(text = "")
        role = role_var.get()
        username_id = login_user.get().lower().strip()
        password = login_pwd.get()
        if not username_id or not password:
            login_status.config(text = "Please fill both fields",
                                foreground = "red")
            return
        if role == "Student":
            if student_login_validation(username_id, password):
                student_dashboard(root, username_id)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                login_status.config(text = "Invalid Student ID or Password",
                                    foreground = "red")
        else:  # Lecturer
            if lecturer_login_validation(username_id, password):
                lecturer_dashboard(root, username_id)
                login_user.delete(0, tk.END)
                login_pwd.delete(0, tk.END)
            else:
                login_status.config(text = "Invalid Lecturer credentials",
                                    foreground = "red")

    ttk.Button(master = login_tab,
              text="Login",
               bootstyle="primary",
              command=do_login,
              width=15).grid(row = 4,
                             column = 0,
                             columnspan = 2,
                             pady = 20)

    # ----- STUDENT SIGNUP TAB -----
    student_tab = ttk.Frame(master = tab)
    tab.add(student_tab,
            text="Student Signup")

    ttk.Label(student_tab,
             text="Student ID:").grid(row=0,
                                      column=0,
                                      pady=5,
                                      padx=10,
                                      sticky="e")
    id_for_student = ttk.Entry(master = student_tab)
    id_for_student.grid(row=0,
               column=1,
               pady=5)

    ttk.Label(master = student_tab,
             text="Full Name:").grid(row=1,
                                     column=0,
                                     pady=5,
                                     padx=10,
                                     sticky="e")
    student_name = ttk.Entry(master = student_tab)
    student_name.grid(row=1,
                      column=1,
                      pady=5)

    ttk.Label(master = student_tab,
             text="Password:").grid(row=2,
                                    column=0,
                                    pady=5,
                                    padx=10,
                                    sticky="e")
    s_password = ttk.Entry(master = student_tab,
                     show="*")
    s_password.grid(row=2,
               column=1,
               pady=5)

    ttk.Label(master = student_tab,
             text="Confirm Password:").grid(row=3,
                                            column=0,
                                            pady=5,
                                            padx=10,
                                            sticky="e")
    studentConfirm_password = ttk.Entry(master = student_tab,
                                       show="*")
    studentConfirm_password.grid(row=3,
                                 column=1,
                                 pady=5)

    ttk.Label(master = student_tab,
              text="Faculty:").grid(row=4,
                                    column=0,
                                    pady=5,
                                    padx=10,
                                    sticky="e")
    faculty_var = ttk.StringVar(value=list(faculty_data.keys())[0])
    faculty_signup_combo = ttk.Combobox(student_tab,
                                        textvariable=faculty_var,
                                        values=list(faculty_data.keys()),
                                        state='readonly',
                                        width=25)
    faculty_signup_combo.grid(row=4,
                              column=1,
                              padx=10,
                              pady=5)

    ttk.Label(master = student_tab,
              text='Program:').grid(row=5,
                                    column=0,
                                    padx=10,
                                    pady=5,
                                    sticky='e')
    program_signup_var = ttk.StringVar()
    program_combo = ttk.Combobox(master = student_tab,
                                 textvariable=program_signup_var,
                                 state='readonly',
                                 width=25)

    # The args allows the function to accept any number of positional arguments, packing them into a tuple(collection of values)
    def update_programs(*args):
        faculty = faculty_var.get()
        programs = list(faculty_data.get(faculty, {}).get('programs', {}).keys())
        program_combo['values'] = programs
        if programs:
            program_signup_var.set(programs[0])
    faculty_signup_combo.bind('<<ComboboxSelected>>',
                              update_programs)
    update_programs()
    program_combo.grid(row=5,
                       column=1,
                       padx=10,
                       pady=5)
    def do_student_signup():
        student_signup_status.config(text="")

        # Get student id, name, password, confirm password, faculty, program
        id_student = id_for_student.get().strip()
        name = student_name.get().strip()
        password = s_password.get()
        confirm_password = studentConfirm_password.get()
        faculty = faculty_var.get()
        program = program_combo.get()

        # Checks if lecturer input id and password, if not, an error message will appear
        if not id_student or not name or not password:
            student_signup_status.config(text="ID, Name and Password required")
            return

        # Checks if password length is less than 8, if it is, an error message will appear
        if len(password) < 8:
            student_signup_status.config(text="Password must be at least 8 characters long")
            return
        if password != confirm_password:
            student_signup_status.config(text="Passwords do not match")
            return
        if register_student(id_student, password, name, faculty, program):
            messagebox.showinfo("Success", f"Student {id_student} registered! You can now log in.")
            id_for_student.delete(0, tk.END)
            student_name.delete(0, tk.END)
            s_password.delete(0, tk.END)
            studentConfirm_password.delete(0, tk.END)
        else:
            student_signup_status.config(text= f"Student ID: {id_student} already exists")

    student_signup_status = ttk.Label(master = student_tab,
                             text="",
                             foreground = "red")
    student_signup_status.grid(row = 6,
                      column = 0,
                      columnspan = 2,
                      pady = 5)

    ttk.Button(master = student_tab,
              text="Register Student",
               bootstyle="primary",
              command=do_student_signup,
              width=18).grid(row = 7,
                             column = 0,
                             columnspan = 2,
                             pady = 15)


    # ----- LECTURER SIGNUP TAB -----
    lecturer_tab = ttk.Frame(master = tab)
    tab.add(lecturer_tab,
            text="Lecturer Signup")

    ttk.Label(master = lecturer_tab,
             text="Username:").grid(row=0,
                                    column=0,
                                    pady=10,
                                    padx=10,
                                    sticky="e")
    lecturer_username = ttk.Entry(master = lecturer_tab)
    lecturer_username.grid(row=0,
                column=1,
                pady=10)

    ttk.Label(master = lecturer_tab,
             text="Password:").grid(row=1,
                                    column=0,
                                    pady=10,
                                    padx=10,
                                    sticky="e")
    lecturer_password = ttk.Entry(master = lecturer_tab,
                                 show="*")
    lecturer_password.grid(row=1,
                           column=1,
                           pady=10)

    ttk.Label(master = lecturer_tab,
             text="Confirm Password:").grid(row=2,
                                            column=0,
                                            pady=10,
                                            padx=10,
                                            sticky="e")
    lecturerConfirm_password = ttk.Entry(master = lecturer_tab,
                                        show="*")
    lecturerConfirm_password.grid(row=2,
                                  column=1,
                                  pady=10)

    def do_lecturer_signup():
        lecturer_signup_status.config(text="")
        user = lecturer_username.get().lower().strip()
        password = lecturer_password.get()
        confirm_password = lecturerConfirm_password.get()

        # Checks if user input username and password, if not, an error message will appear
        if not user or not password:
            lecturer_signup_status.config(text="Username and password required")
            return

        # Checks if user length is less than 5, if it is, an error message will appear
        if len(user) < 5:
            lecturer_signup_status.config(text="Username is too short. Must be at least 5 characters long")
            return

        # Checks if password length is less than 8, if it is, an error message will appear
        if len(password) < 8:
            lecturer_signup_status.config(text="Password must be at least 8 characters long")
            return

        # Checks if password and confirm password are the same
        if password != confirm_password:
            lecturer_signup_status.config(text="Passwords do not match")
            return

        # If all the credential are correct, you will login
        if register_lecturer(user, password):
            messagebox.showinfo("Success", f"Lecturer {user} registered! You can now log in.")
            lecturer_username.delete(0, tk.END)
            lecturer_password.delete(0, tk.END)
            lecturerConfirm_password.delete(0, tk.END)
        else:
            lecturer_signup_status.config(text=f"Username: {user} already taken")

    lecturer_signup_status = ttk.Label(master=lecturer_tab,
                                      text="",
                                      foreground="red")
    lecturer_signup_status.grid(row=3,
                               column=0,
                               columnspan=2,
                               pady=5)

    ttk.Button(master = lecturer_tab,
              text="Register Lecturer",
              bootstyle="primary",
              command=do_lecturer_signup,
              width=18).grid(row=4,
                             column=0,
                             columnspan=2,
                             pady=20)

    root.mainloop()
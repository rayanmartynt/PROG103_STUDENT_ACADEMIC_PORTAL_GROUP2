from logic import *

# Calculate grades
print(calculate_total(80,80,80,80))

#Register student and lecturer
print(register_student('905005656', 'Rmt123', 'Rayan', 'FICT', 'BSEM'))
print(register_lecturer('lecturer', '123'))

# Checks for validation
print(student_login_validation('905005656', 'Rmt123')) # Prints True because the id and password matches the one registered with
print(lecturer_login_validation('lecture', '123')) # Prints False because the user is not spelled correctly

# Add and get grades from the student with the studentID 905005656
print(add_grade('905005656', '1', 'FICT', 'Database', 80, 80, 80, 80))
print(get_student_grades('905005656'))

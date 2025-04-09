import csv
import os
import matplotlib.pyplot as plt
from tabulate import tabulate

# File paths for data storage
STUDENT_FILE = 'students.csv'
TEACHER_FILE = 'teachers.csv'
COURSE_FILE = 'courses.csv'

# Global variables to store data
students = []
teachers = []
courses = []

# Management password
MANAGEMENT_PASSWORD = "AMMA"

# Function to load data from a CSV file
def load_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]

# Function to save data to a CSV file
def save_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to load all data into memory and sort by ID
def load_data():
    global students, teachers, courses
    students = sorted(load_csv(STUDENT_FILE), key=lambda x: int(x['student_id']))
    for student in students:
        student['student_id'] = int(student['student_id'])
        student['age'] = int(student['age'])
        student['cgpa'] = float(student['cgpa'])
        student['attendance'] = float(student['attendance'])
        student['courses'] = eval(student['courses']) if 'courses' in student and student['courses'] else []

    teachers = sorted(load_csv(TEACHER_FILE), key=lambda x: int(x['teacher_id']))
    for teacher in teachers:
        teacher['teacher_id'] = int(teacher['teacher_id'])

    courses = sorted(load_csv(COURSE_FILE), key=lambda x: int(x['course_id']))
    for course in courses:
        course['course_id'] = int(course['course_id'])
        course['teacher_id'] = int(course['teacher_id'])
        course['students'] = eval(course['students']) if 'students' in course and course['students'] else []

# Function to save all data from memory to CSV files
def save_data():
    save_csv(STUDENT_FILE, students, ['student_id', 'name', 'age', 'cgpa', 'attendance', 'courses'])
    save_csv(TEACHER_FILE, teachers, ['teacher_id', 'name', 'subject'])
    save_csv(COURSE_FILE, courses, ['course_id', 'name', 'teacher_id', 'students'])

# Function to plot student CGPAs
def plot_student_cgpa():
    if not students:
        print("No student data available to plot.")
        return
    
    student_ids = [student['student_id'] for student in students]
    cgpas = [student['cgpa'] for student in students]
    
    plt.figure(figsize=(10, 6))
    plt.bar(student_ids, cgpas, color='skyblue')
    plt.xlabel("Student ID")
    plt.ylabel("CGPA")
    plt.title("Student CGPAs")
    plt.show()

# Function to view students in tabulated form
def view_students():
    if not students:
        print("No students found.")
        return
    headers = ["Student ID", "Name", "Age", "CGPA", "Attendance", "Courses"]
    table_data = [[student['student_id'], student['name'], student['age'], student['cgpa'], student['attendance'], student['courses']] for student in students]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

# Function to view teachers in tabulated form
def view_teachers():
    if not teachers:
        print("No teachers found.")
        return
    headers = ["Teacher ID", "Name", "Subject"]
    table_data = [[teacher['teacher_id'], teacher['name'], teacher['subject']] for teacher in teachers]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

# Function to view a student's profile and enrolled courses
def view_student_profile(student_id):
    student = next((s for s in students if s['student_id'] == student_id), None)
    if student:
        headers = ["Attribute", "Value"]
        profile_data = [
            ["ID", student['student_id']],
            ["Name", student['name']],
            ["Age", student['age']],
            ["CGPA", student['cgpa']],
            ["Attendance", student['attendance']]
        ]
        print(tabulate(profile_data, headers=headers, tablefmt="pretty"))
        
        # Display enrolled courses
        enrolled_courses = [course for course in courses if course['course_id'] in student['courses']]
        if enrolled_courses:
            print("\nEnrolled Courses:")
            headers = ["Course ID", "Course Name", "Teacher ID"]
            course_data = [[course['course_id'], course['name'], course['teacher_id']] for course in enrolled_courses]
            print(tabulate(course_data, headers=headers, tablefmt="pretty"))
        else:
            print("\nNo enrolled courses.")
    else:
        print("Student not found!")

# Function to add a student
def add_student():
    try:
        student_id = int(input("Enter student ID: "))
        if any(student['student_id'] == student_id for student in students):
            print("Error: Student ID already exists.")
            return

        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        cgpa = float(input("Enter student CGPA: "))
        attendance = float(input("Enter student attendance percentage: "))
        student = {'student_id': student_id, 'name': name, 'age': age, 'cgpa': cgpa, 'attendance': attendance, 'courses': []}
        students.append(student)
        students.sort(key=lambda x: x['student_id'])  # Sort by student_id after adding
        save_data()
        print(f"Added Student: {student}")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Function to remove a student
def remove_student():
    try:
        student_id = int(input("Enter student ID to remove: "))
        global students
        students = [s for s in students if s['student_id'] != student_id]
        save_data()
        print(f"Removed Student with ID: {student_id}")
    except ValueError:
        print("Invalid ID. Please enter a numeric ID.")

# Function to add a teacher
def add_teacher():
    try:
        teacher_id = int(input("Enter teacher ID: "))
        if any(teacher['teacher_id'] == teacher_id for teacher in teachers):
            print("Error: Teacher ID already exists.")
            return

        name = input("Enter teacher name: ")
        subject = input("Enter subject: ")
        teacher = {'teacher_id': teacher_id, 'name': name, 'subject': subject}
        teachers.append(teacher)
        save_data()
        print(f"Added Teacher: {teacher}")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Function to add a course
def add_course():
    try:
        course_id = int(input("Enter course ID: "))
        if any(course['course_id'] == course_id for course in courses):
            print("Error: Course ID already exists.")
            return

        name = input("Enter course name: ")
        teacher_id = int(input("Enter teacher ID: "))
        teacher = next((t for t in teachers if t['teacher_id'] == teacher_id), None)
        if teacher:
            course = {'course_id': course_id, 'name': name, 'teacher_id': teacher_id, 'students': []}
            courses.append(course)
            save_data()
            print(f"Added Course: {course}")
        else:
            print("Teacher not found!")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Function to enroll a student in a course
def enroll_student_in_course():
    try:
        student_id = int(input("Enter student ID to enroll: "))
        student = next((s for s in students if s['student_id'] == student_id), None)
        
        if not student:
            print("Student not found!")
            return

        course_id = int(input("Enter course ID to enroll in: "))
        course = next((c for c in courses if c['course_id'] == course_id), None)

        if not course:
            print("Course not found!")
            return

        if course_id in student['courses']:
            print("Student is already enrolled in this course.")
            return

        student['courses'].append(course_id)
        course['students'].append(student_id)
        
        save_data()
        print(f"Enrolled Student {student_id} in Course {course_id}.")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Function to update a student's information
def update_student():
    try:
        student_id = int(input("Enter the student ID to update: "))
        student = next((s for s in students if s['student_id'] == student_id), None)
        
        if not student:
            print("Student not found!")
            return

        print("Enter new information (leave blank to keep the current value):")
        
        # Update name
        name = input(f"Name ({student['name']}): ").strip()
        if name:
            student['name'] = name

        # Update age
        age_input = input(f"Age ({student['age']}): ").strip()
        if age_input:
            student['age'] = int(age_input)
        
        # Update CGPA
        cgpa_input = input(f"CGPA ({student['cgpa']}): ").strip()
        if cgpa_input:
            student['cgpa'] = float(cgpa_input)
        
        # Update attendance
        attendance_input = input(f"Attendance ({student['attendance']}): ").strip()
        if attendance_input:
            student['attendance'] = float(attendance_input)

        # Update courses
        courses_input = input(f"Courses (Current: {student['courses']}): ").strip()
        if courses_input:
            try:
                student['courses'] = eval(courses_input)
            except:
                print("Invalid format for courses. Please enter a list of course IDs (e.g., [1, 2, 3]).")
                return
        
        save_data()
        print("Student information updated successfully.")
    except ValueError:
        print("Invalid input. Please enter valid data.")

# Management interface function
def management_interface():
    password = input("Enter Management Password: ")
    if password != MANAGEMENT_PASSWORD:
        print("Incorrect password. Access denied.")
        return

    while True:
        print("\nManagement Interface:")
        print("1. Add Student\n2. View Students\n3. Remove Student\n4. Add Teacher")
        print("5. View Teachers\n6. Add Course\n7. Enroll Student in Course\n8. Plot Student CGPAs")
        print("9. Update Student\n10. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            remove_student()
        elif choice == "4":
            add_teacher()
        elif choice == "5":
            view_teachers()
        elif choice == "6":
            add_course()
        elif choice == "7":
            enroll_student_in_course()
        elif choice == "8":
            plot_student_cgpa()
        elif choice == "9":
            update_student()
        elif choice == "10":
            print("Exiting Management Interface.")
            break
        else:
            print("Invalid choice.")

# Student interface function
# Student interface function
def student_interface():
    try:
        student_id = int(input("Enter your Student ID: "))
        student = next((s for s in students if s['student_id'] == student_id), None)
                
        if not student:
            print("Student not found!")
            return

        while True:
            print("\nStudent Interface:")
            print("1. View Profile\n2. Enroll in Course\n3. View Enrolled Courses\n4. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                view_student_profile(student_id)  # Display full profile with courses
            elif choice == "2":
                enroll_student_in_course()
            elif choice == "3":
                view_student_profile(student_id)  # Optionally remove this as "View Profile" covers it
            elif choice == "4":
                print("Exiting Student Interface.")
                break
            else:
                print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a valid Student ID.")


# Load data at the start
load_data()

# Main interface function
def main_interface():
    while True:
        print("\nMain Interface:")
        print("1. Management Interface\n2. Student Interface\n3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            management_interface()
        elif choice == "2":
            student_interface()
        elif choice == "3":
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")

# Run the main interface
main_interface()
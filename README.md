# 🎓 Grade Hub

**A Python‑based GUI application to manage student grades – built for Sierra Leone Universities, aligned with SDG 4 (Quality Education).**


## 📌 Overview

The **Grade Hub** is a desktop application that helps students and lecturers work together more effectively in universities accros Sierra Leone.  
Lecturers can upload test (20%), assignment (15%), project (30%), and exam (35%) scores. The system automatically calculates weighted totals and letter grades. Students can log in with their ID to view their own semester‑by‑semester results.

This project was created as the final submission for the **Principles of Structured Programming** course. It demonstrates modular design, clean GUI logic, and real‑world problem solving.

## ✨ Features

### For Students

- **Secure login** using Student ID and password  
- **View all personal grades** organised by semester and module  
- See **individual marks** for test, assignment, project, and exam  
- Instantly see the **calculated total** (weighted) and **letter grade** (A+ to F)  
- **Refresh** the grade table to fetch the latest updates from lecturers  
- **Logout** safely to return to the login screen  

### For Lecturers

- **Secure login** using username and password  
- **Upload grades** for any registered student  
- Choose from **6 semesters** (Semester 1 – 6) and **10 modules** (e.g., Structured Programming, Database, etc.)  
- Enter marks for: **Test (20%)**, **Assignment (15%)**, **Project (30%)**, **Exam (35%)**  
- **Preview** the weighted total and letter grade **before saving**  
- **Save grade** – updates the system; if a grade for the same student/semester/module exists, it is overwritten  
- **View all grades** in the system (every student, every module) in a single table  
- **Refresh** the grade table to see the latest saved records  
- **Logout** safely  

### General & Technical Features

- **Clean, modern GUI** using `ttkbootstrap` (morph theme) – no terminal interaction needed  
- **In‑memory data storage** with Python dictionaries and lists (easy to understand, no external database required)  
- **Structured programming** – uses functions, loops, decision structures, and modular design  
- **Real‑world alignment** – built for University of Sierra Leone  
- **Supports SDG 4** (Quality Education) by digitising academic records
  

## 👥 Authors

- **Rayan Martin Turay**  
- **Abdul Karim Koroma**  
- **Foday Kamara**


## 🌍 Real‑World Impact

- Built for **Sierra Leone**’s educational system
- Supports **SDG 4 – Quality Education** by digitising grade management, making academic records more transparent and accessible.


## 🧰 Technology Stack

- **Language:** Python 3  
- **GUI:** `tkinter` + `ttkbootstrap` (themed widgets)  
- **Data storage:** Python dictionaries & lists (temporary, in‑memory)  
- **License:** MIT


## 📸 Screenshots
- **Login Page**

  <img width="496" height="536" alt="Screenshot 2026-06-13 021730" src="https://github.com/user-attachments/assets/20e95837-b715-4518-a3cf-e22012a1e90c" />

- **Student Signup Page**

  <img width="495" height="550" alt="Screenshot 2026-06-13 021819" src="https://github.com/user-attachments/assets/fa337724-d5ba-4f84-af96-5c1f51238a08" />

- **Lecturer Signup Page**

  <img width="491" height="545" alt="Screenshot 2026-06-13 021807" src="https://github.com/user-attachments/assets/89add04b-025b-4846-8448-2b2ad3335d8d" />

- **Lecturer Dashboard**
  
  <img width="847" height="585" alt="Screenshot 2026-06-13 022637" src="https://github.com/user-attachments/assets/dbea4e92-5b6c-417f-aff9-e9d2cb8e52f0" />

- **Student Dashboard**

  <img width="941" height="441" alt="Screenshot 2026-06-13 022649" src="https://github.com/user-attachments/assets/78ae9245-abb1-40de-b84f-f2ed8c15ceee" />

## 🚀 How to Run the Project

### 1. Prerequisites

Make sure you have Python 3 installed on your computer. Then install the extra library `ttkbootstrap`:

```bash
pip install ttkbootstrap
```
### 2. Download the code

```bash
git clone https://github.com/rayanmartyn/PROG103_STUDENT_ACADEMIC_PORTAL_GROUP2.git
cd PROG103_STUDENT_ACADEMIC_PORTAL_GROUP2
cd src
```
### 3. Run the application

```bash
python main.py
```

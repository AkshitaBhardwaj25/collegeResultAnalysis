# 🎓 College Result Analysis System

A full-stack data analytics project built using **Python, MySQL, and Streamlit** to manage, analyze, and visualize college examination results.

---

## Features

### Core Functionality

* Student & Result Management (CRUD operations)
* Course, Exam, Department data handling
* Automated grade & pass/fail calculation (via triggers)

### Analytics & Insights

* Topper analysis (semester-wise, department-wise)
* Subject-wise average marks
* Pass rate by department
* Grade distribution per course
* Course performance trends over semesters
* GPA calculation (SQL function + Python)

### Advanced Database Integration

* Stored Procedures (e.g., `RecomputeAllGrades`)
* Cursor-based procedures
* SQL Function: `CalculateGPA`
* Optimized queries with joins and aggregations

### Visualization

* Bar charts (Top subjects, pass rates)
* Trend analysis graphs using Matplotlib

### Export Utilities

* Export data to CSV
* Export data to Excel

---

## Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** MySQL
* **Libraries:** pandas, matplotlib, mysql-connector-python, python-dotenv, altair

---

## 📂 Project Structure

```
DBMS_PROJECT/
│
├── frontend.py        # Streamlit UI
├── college_result_system.py    # Backend logic
├── schema.sql                 # Database schema
├── requirements.txt           # Dependencies
├── README.md
└── .gitignore
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/AkshitaBhardwaj25/collegeResultAnalysis.git
cd collegeResultAnalysis
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Setup Database

Create database:

```
CREATE DATABASE college_results;
```

Import schema:

```
mysql -u root -p college_results < schema.sql
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=college_results
```

---

### 5. Run Application

```
streamlit run frontend.py
```

---

## Sample Functionalities

* View dashboard stats (students, courses, exams)
* Analyze top-performing students
* Visualize pass percentages across departments
* Track subject performance trends

---

## Security Practices

* Used environment variables (`.env`) for database credentials
* Avoided hardcoding sensitive information
* Added `.gitignore` to exclude private files

---

## 👩‍💻 Author

**Akshita**
---

## Note

This project is built for academic purposes and demonstrates:

* Database design
* Backend integration
* Data analytics & visualization
* Real-world project structuring

---

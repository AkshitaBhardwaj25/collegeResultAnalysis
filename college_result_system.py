"""
college_result_system.py

Professional, cleaned backend for College Exam Result Analysis (MySQL + Python)

Features (high level):
 - Robust DB connection with retries and logging
 - Safe execute / batch execute helpers
 - DataFrame helpers (pandas)
 - CRUD for Student, Result
 - Rich analytics (toppers, subject averages, pass rates, grade distributions, gender analysis)
 - Plotting helpers (matplotlib)
 - Export utilities (CSV, Excel)
 - PL/SQL integration: calls to stored procedures, cursor procedure, and SQL function CalculateGPA
 - CLI / quick-summary helpers for viva/demo
"""
# college_result_system.py  (fixed)
import os
import time
import csv
import io
import logging
from typing import Any, Dict, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Configuration
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Div_09_ya_11",
    "database": "college_results",
    "raise_on_warnings": True,
    "autocommit": False
}

# ----------------------------
# Logging
# ----------------------------
LOG_FILE = "college_result_system.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
logging.getLogger().addHandler(console_handler)

# ----------------------------
# Low-level DB helpers
# ----------------------------
def get_connection(retries: int = 2, delay: float = 0.5) -> mysql.connector.connection_cext.CMySQLConnection:
    last_exc = None
    for attempt in range(retries + 1):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                logging.debug("Connected to MySQL on attempt %d", attempt + 1)
                return conn
        except Error as e:
            last_exc = e
            logging.warning("DB connection attempt %d failed: %s", attempt + 1, e)
            time.sleep(delay)
    logging.error("Failed to connect to DB after %d attempts: %s", retries + 1, last_exc)
    raise last_exc

def execute_sql(sql: str, params: Tuple = None, fetch: bool = False) -> Optional[List[Dict[str, Any]]]:
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        logging.debug("Executing SQL: %s -- params: %s", sql.strip().splitlines()[0], params)
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        if fetch:
            rows = cur.fetchall()
            logging.debug("Fetched %d rows", len(rows))
            return rows
        conn.commit()
    except Error as e:
        logging.exception("SQL execution error: %s -- SQL: %s -- Params: %s", e, sql, params)
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return None

def execute_many(sql: str, params_list: List[Tuple]):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.executemany(sql, params_list)
        conn.commit()
        logging.info("Batch executed %d rows.", len(params_list))
    except Error as e:
        logging.exception("Batch execution error: %s", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ----------------------------
# DataFrame helpers
# ----------------------------
def df_from_query(sql: str, params: Tuple = None) -> pd.DataFrame:
    conn = None
    try:
        conn = get_connection()
        df = pd.read_sql(sql, conn, params=params)
        return df
    except Exception as e:
        logging.exception("Failed to build DataFrame from query: %s -- %s", sql, e)
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# ----------------------------
# Dashboard helpers (kept)
# ----------------------------
def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT
            (SELECT COUNT(*) FROM Student) AS student_count,
            (SELECT COUNT(*) FROM Course) AS course_count,
            (SELECT COUNT(*) FROM Exam) AS exam_count,
            (SELECT ROUND(AVG(MarksObtained),2) FROM Result) AS avg_marks,
            (SELECT ROUND(AVG(CASE WHEN Status='Pass' THEN 1 ELSE 0 END)*100,2) FROM Result) AS pass_rate
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def get_top_10_subjects():
    sql = """
        SELECT C.CourseID, C.CourseCode, C.CourseName,
               ROUND(AVG(R.MarksObtained), 2) AS AvgMarks,
               COUNT(*) AS Attempts
        FROM Result R
        JOIN Course C ON R.CourseID = C.CourseID
        GROUP BY C.CourseID, C.CourseCode, C.CourseName
        ORDER BY AvgMarks DESC
        LIMIT 10
    """
    return df_from_query(sql)

# ----------------------------
# CRUD: Student
# ----------------------------
def get_all_students() -> pd.DataFrame:
    sql = "SELECT StudentID, RollNo, Name, Gender, DOB, DepartmentID, BatchYear, Email, Phone FROM Student ORDER BY StudentID;"
    return df_from_query(sql)

def get_student(student_id: int) -> Optional[Dict[str, Any]]:
    rows = execute_sql("SELECT * FROM Student WHERE StudentID = %s", (student_id,), fetch=True)
    return rows[0] if rows else None

def add_student(roll: str, name: str, gender: str, dob: str, dept: int, batch: int, email: str, phone: str):
    sql = """
    INSERT INTO Student (RollNo, Name, Gender, DOB, DepartmentID, BatchYear, Email, Phone)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    execute_sql(sql, (roll, name, gender, dob, dept, batch, email, phone))
    logging.info("Added student: %s (%s)", name, roll)

def update_student(student_id: int, **fields):
    if not fields:
        logging.info("update_student called with no fields for %s", student_id)
        return
    allowed = {'RollNo','Name','Gender','DOB','DepartmentID','BatchYear','Email','Phone'}
    sets = []
    params = []
    for k, v in fields.items():
        if k in allowed:
            sets.append(f"{k}=%s")
            params.append(v)
    if not sets:
        logging.warning("No allowed fields provided for update_student")
        return
    params.append(student_id)
    sql = f"UPDATE Student SET {', '.join(sets)} WHERE StudentID=%s"
    execute_sql(sql, tuple(params))
    logging.info("Updated student %d fields: %s", student_id, list(fields.keys()))

def delete_student(student_id: int):
    # Delete results first (if you prefer cascade use DB constraint)
    execute_sql("DELETE FROM Result WHERE StudentID = %s", (student_id,))
    execute_sql("DELETE FROM Student WHERE StudentID = %s", (student_id,))
    logging.info("Deleted student and results for StudentID %d", student_id)

# ----------------------------
# CRUD: Result (trigger handles Grade & Status)
# ----------------------------
def add_result(student_id: int, course_id: int, exam_id: int, marks: float, max_marks: float = 100.0):
    sql = "INSERT INTO Result (StudentID, CourseID, ExamID, MarksObtained, MaxMarks) VALUES (%s,%s,%s,%s,%s)"
    execute_sql(sql, (student_id, course_id, exam_id, marks, max_marks))
    logging.info("Inserted Result: S:%s C:%s E:%s Marks:%s", student_id, course_id, exam_id, marks)

def update_marks(student_id: int, course_id: int, exam_id: int, new_marks: float):
    # keep column names consistent with DB schema (CourseID)
    sql = "UPDATE Result SET MarksObtained = %s WHERE StudentID = %s AND CourseID = %s AND ExamID = %s"
    execute_sql(sql, (new_marks, student_id, course_id, exam_id))
    logging.info("Updated marks for StudentID %s CourseID %s ExamID %s -> %s", student_id, course_id, exam_id, new_marks)

def delete_result(result_id: int):
    execute_sql("DELETE FROM Result WHERE ResultID = %s", (result_id,))
    logging.info("Deleted ResultID %s", result_id)

# ----------------------------
# Utility list functions
# ----------------------------
def list_courses() -> pd.DataFrame:
    return df_from_query("SELECT CourseID, CourseCode, CourseName, DepartmentID, Credits, Semester FROM Course ORDER BY CourseCode;")

def list_exams() -> pd.DataFrame:
    return df_from_query("SELECT ExamID, ExamName, ExamType, AcademicYear, Semester, ExamDate FROM Exam ORDER BY ExamDate DESC;")

def list_departments() -> pd.DataFrame:
    return df_from_query("SELECT DepartmentID, DepartmentName, HOD FROM Department ORDER BY DepartmentID;")

def list_faculty() -> pd.DataFrame:
    return df_from_query("SELECT FacultyID, Name, DepartmentID, Email, Phone FROM Faculty ORDER BY FacultyID;")

# ----------------------------
# Analytics functions
# ----------------------------
def get_topper_by_semester(semester: int, top_n: int = 10) -> pd.DataFrame:
    sql = """
    SELECT S.StudentID, S.RollNo, S.Name,
           ROUND(AVG(R.MarksObtained),2) AS AvgMarks,
           COUNT(*) AS ExamsTaken
    FROM Result R
    JOIN Student S ON R.StudentID = S.StudentID
    JOIN Course C ON R.CourseID = C.CourseID
    JOIN Exam E ON R.ExamID = E.ExamID
    WHERE E.Semester = %s
    GROUP BY S.StudentID
    ORDER BY AvgMarks DESC
    LIMIT %s
    """
    return df_from_query(sql, (semester, top_n))

def subject_wise_average() -> pd.DataFrame:
    sql = """
    SELECT C.CourseID, C.CourseCode, C.CourseName, ROUND(AVG(R.MarksObtained),2) AS AvgMarks, COUNT(*) AS Entries
    FROM Result R
    JOIN Course C ON R.CourseID = C.CourseID
    GROUP BY C.CourseID, C.CourseCode, C.CourseName
    ORDER BY AvgMarks DESC;
    """
    return df_from_query(sql)

def pass_rate_by_department() -> pd.DataFrame:
    sql = """
    SELECT D.DepartmentID, D.DepartmentName,
           ROUND(AVG(CASE WHEN R.Status='Pass' THEN 1.0 ELSE 0.0 END) * 100.0, 2) AS PassPercent,
           COUNT(*) AS Total
    FROM Result R
    JOIN Student S ON R.StudentID = S.StudentID
    JOIN Department D ON S.DepartmentID = D.DepartmentID
    GROUP BY D.DepartmentID
    ORDER BY PassPercent DESC;
    """
    return df_from_query(sql)

def grade_distribution_for_course(course_id: int) -> pd.DataFrame:
    sql = """
    SELECT R.Grade, COUNT(*) AS Count
    FROM Result R
    WHERE R.CourseID = %s
    GROUP BY R.Grade
    ORDER BY FIELD(R.Grade, 'A+','A','B+','B','C','D','F')
    """
    return df_from_query(sql, (course_id,))

def student_gpa_python(student_id: int) -> float:
    sql = """
    SELECT ROUND(SUM(C.Credits * 
        (CASE R.Grade WHEN 'A+' THEN 10 WHEN 'A' THEN 9 WHEN 'B+' THEN 8 WHEN 'B' THEN 7 WHEN 'C' THEN 6 WHEN 'D' THEN 5 ELSE 0 END))
        / SUM(C.Credits), 2) AS GPA
    FROM Result R
    JOIN Course C ON R.CourseID = C.CourseID
    WHERE R.StudentID = %s
    """
    df = df_from_query(sql, (student_id,))
    if df.empty or df.iloc[0]['GPA'] is None:
        return 0.0
    return float(df.iloc[0]['GPA'])

def department_toppers(department_id:int, top_n:int=5) -> pd.DataFrame:
    sql = """
    SELECT S.StudentID, S.RollNo, S.Name,
           ROUND(AVG(R.MarksObtained),2) AS AvgMarks
    FROM Result R
    JOIN Student S ON R.StudentID = S.StudentID
    WHERE S.DepartmentID = %s
    GROUP BY S.StudentID
    ORDER BY AvgMarks DESC
    LIMIT %s
    """
    return df_from_query(sql, (department_id, top_n))

def course_trend(course_id:int) -> pd.DataFrame:
    sql = """
    SELECT E.Semester, ROUND(AVG(R.MarksObtained),2) AS AvgMarks
    FROM Result R
    JOIN Exam E ON R.ExamID = E.ExamID
    WHERE R.CourseID = %s
    GROUP BY E.Semester
    ORDER BY E.Semester
    """
    return df_from_query(sql, (course_id,))

# ----------------------------
# PL/SQL Integration (Stored Procedures / Cursor / Function calls)
# ----------------------------
def call_recompute_all_grades():
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc("RecomputeAllGrades")
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Called stored procedure: RecomputeAllGrades")

def call_update_course_averages_cursor():
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc("UpdateCourseAveragesCursor")
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Called stored procedure: UpdateCourseAveragesCursor")

def call_update_grades_cursor():
    logging.debug("Alias call_update_grades_cursor -> call_update_course_averages_cursor")
    return call_update_course_averages_cursor()

def get_gpa_from_function(student_id: int) -> Optional[float]:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT CalculateGPA(%s)", (student_id,))
        row = cur.fetchone()
        if row:
            logging.debug("CalculateGPA(%s) -> %s", student_id, row[0])
            return float(row[0]) if row[0] is not None else None
    except Error as e:
        logging.exception("Error calling CalculateGPA: %s", e)
    finally:
        cur.close()
        conn.close()
    return None

# ----------------------------
# CourseStats helpers
# ----------------------------
def get_course_stats() -> pd.DataFrame:
    return df_from_query("SELECT CourseID, AvgMarks, LastUpdated FROM CourseStats ORDER BY CourseID;")

# ----------------------------
# Export utilities
# ----------------------------
def export_df_to_csv_string(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)

def export_df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    bio = io.BytesIO()
    with pd.ExcelWriter(bio, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return bio.getvalue()

# ----------------------------
# Plotting helpers (matplotlib)
# ----------------------------
def plot_subject_bar(df: pd.DataFrame, top_n: int = 10, show: bool = False):
    if df.empty:
        logging.warning("plot_subject_bar: empty dataframe")
        return None
    df_plot = df.head(top_n)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(df_plot['CourseCode'], df_plot['AvgMarks'])
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Average Marks")
    ax.set_title(f"Top {top_n} Courses by Average Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if show:
        plt.show()
    return fig

def plot_pass_rate(df: pd.DataFrame, show: bool = False):
    if df.empty:
        logging.warning("plot_pass_rate: empty dataframe")
        return None
    df_plot = df.sort_values('PassPercent')
    fig, ax = plt.subplots(figsize=(8,5))
    ax.barh(df_plot['DepartmentName'], df_plot['PassPercent'])
    ax.set_xlabel("Pass percent")
    ax.set_title("Pass Rate by Department")
    plt.tight_layout()
    if show:
        plt.show()
    return fig

# ----------------------------
# Batch utilities (for demo)
# ----------------------------
def batch_insert_students(students: List[Tuple[str, str, str, str, int, int, str, str]]):
    sql = """
    INSERT INTO Student (RollNo, Name, Gender, DOB, DepartmentID, BatchYear, Email, Phone)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    execute_many(sql, students)
    logging.info("Batch inserted %d students", len(students))

def batch_insert_results(results: List[Tuple[int,int,int,float,float]]):
    sql = "INSERT INTO Result (StudentID, CourseID, ExamID, MarksObtained, MaxMarks) VALUES (%s,%s,%s,%s,%s)"
    execute_many(sql, results)
    logging.info("Batch inserted %d results", len(results))

# ----------------------------
# Utility: quick_summary for viva
# ----------------------------
def quick_summary() -> Dict[str,int]:
    out = {}
    for name in ['Student','Course','Exam','Department','Faculty','Result']:
        rows = execute_sql(f"SELECT COUNT(*) AS cnt FROM {name}", fetch=True)
        out[name] = rows[0]['cnt'] if rows else 0
    logging.info("Quick summary: %s", out)
    return out

# ----------------------------
# Helpful CLI demo (when run directly)
# ----------------------------
if __name__ == "__main__":
    logging.info("college_result_system.py — quick demo")
    print("Quick counts:", quick_summary())
    print("\nSubject averages (top 5):")
    print(subject_wise_average().head())
    print("\nPass rates:")
    print(pass_rate_by_department().head())
    try:
        courses = list_courses()
        if not courses.empty:
            cid = courses.iloc[0]['CourseID']
            print(course_trend(cid))
    except Exception:
        pass

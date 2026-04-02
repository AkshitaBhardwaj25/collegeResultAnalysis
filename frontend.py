"""
Streamlit frontend for the College Exam Result Analysis project.

Includes:
 - MySQL backend via `college_result_system.py`
 - Integration with stored procedures, cursor procedure, GPA SQL function
 - CourseStats dashboard (generated via cursor)
 - Top subjects chart restored
"""

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import io
import time

# Import backend
from college_result_system import (
    get_all_students, get_topper_by_semester, subject_wise_average,
    add_student, update_student, delete_student, add_result, update_marks,
    list_courses, list_exams, list_departments, list_faculty,
    pass_rate_by_department, grade_distribution_for_course,
    department_toppers, course_trend, plot_subject_bar,
    quick_summary, export_df_to_csv_string, export_df_to_excel_bytes,
    call_recompute_all_grades, call_update_course_averages_cursor,
    get_gpa_from_function, get_course_stats
)
from college_result_system import get_dashboard_stats, get_top_10_subjects


st.set_page_config(page_title="College Results Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---------------------
# Helper utilities
# ---------------------
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    return export_df_to_excel_bytes(df)

def clean_avg_marks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace None/NaN AvgMarks with 0 (or 'No Data').
    Prevents Altair/matplotlib from crashing.
    """
    if "AvgMarks" in df.columns:
        df["AvgMarks"] = df["AvgMarks"].fillna(0)
    return df

# ---------------------
# Sidebar Navigation
# ---------------------
page = st.sidebar.radio("Go to", [
    "Home", "Students", "Toppers & Rankings",
    "Subjects & Analysis", "Modify Records",
    "Export & Utilities", "Dashboard", "Help"
])

st.title("College Exam Result Analysis")

# ---------------------
# HOME
# ---------------------

if page == "Home":
    st.header("Overview & Quick Summary")
    summary = quick_summary()
    cols = st.columns(4)
    cols[0].metric("Students", summary.get("Student", 0))
    cols[1].metric("Courses", summary.get("Course", 0))
    cols[2].metric("Exams", summary.get("Exam", 0))
    cols[3].metric("Results", summary.get("Result", 0))

    st.markdown("---")
    st.subheader("Recent Student Data")
    st.dataframe(get_all_students().head(20), use_container_width=True)
    
# ---------------------
# Dashboard
# ---------------------

elif page == "Dashboard":
    st.header("Overall Dashboard")

    stats = get_dashboard_stats()
    if stats:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Students", stats["student_count"])
        c2.metric("Courses", stats["course_count"])
        c3.metric("Exams", stats["exam_count"])
        c4.metric("Avg Marks", stats["avg_marks"])
        c5.metric("Pass Rate (%)", stats["pass_rate"])

    st.markdown("---")
    st.subheader("Top 10 Subjects")

    df_top = get_top_10_subjects()
    st.dataframe(df_top)

    chart = alt.Chart(df_top).mark_bar().encode(
        x="CourseCode",
        y="AvgMarks",
        tooltip=["CourseCode", "CourseName", "AvgMarks", "Attempts"],
        color="AvgMarks"
    )
    st.altair_chart(chart, use_container_width=True)

# ---------------------
# STUDENTS
# ---------------------
elif page == "Students":
    st.header("Students")
    with st.spinner("Fetching data..."):
        try:
            df = get_all_students()
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.error("Failed to fetch student data. Check database connection.")

    st.markdown("---")
    st.subheader("Search / View Details")
    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input("Search by name")
        if search:
            st.dataframe(df[df['Name'].str.contains(search, case=False)])

    with col2:
        sid = st.number_input("Enter Student ID", min_value=0)
        if sid > 0:
            info = df[df["StudentID"] == sid]
            if not info.empty:
                record = info.to_dict(orient="records")[0]
                for k, v in record.items():
                    if hasattr(v, "isoformat"):
                        record[k] = v.isoformat()
                st.json(record)

                st.markdown("### GPA (via SQL Function CalculateGPA)")
                gpa = get_gpa_from_function(int(sid))
                if gpa is not None:
                    st.success(f"GPA = {gpa}")
                else:
                    st.warning("GPA not available")
            else:
                st.warning("No student found.")

# ---------------------
# TOPPERS
# ---------------------
elif page == "Toppers & Rankings":
    st.header("Toppers & Rankings")
    col1, col2 = st.columns([2, 1])

    with col1:
        semester = st.number_input("Semester", 1, 8, 1)
        topn = st.slider("Top N", 3, 50, 10)
        if st.button("Show Toppers"):
            df_top = get_topper_by_semester(semester, topn)
            st.dataframe(df_top)
            if not df_top.empty:
                st.download_button("Download CSV", df_to_csv_bytes(df_top),
                                   file_name=f"toppers_sem{semester}.csv")

    with col2:
        st.subheader("Department Toppers")
        deps = list_departments()
        if not deps.empty:
            did = st.selectbox("Department", deps['DepartmentID'],
                format_func=lambda x: deps[deps['DepartmentID']==x]['DepartmentName'].values[0])
            topn2 = st.number_input("Top N", 1, 20, 5)
            if st.button("Show Dept Toppers"):
                st.dataframe(department_toppers(did, topn2))

# ---------------------
# SUBJECTS & ANALYSIS
# ---------------------
elif page == "Subjects & Analysis":
    st.header("Subject-wise Analysis")
    df_sub = subject_wise_average()
    st.dataframe(df_sub)

    st.markdown("---")
    st.subheader("Course Trends")
    courses = list_courses()
    if not courses.empty:
        cid = st.selectbox("Select Course", courses["CourseID"],
            format_func=lambda x: courses[courses["CourseID"]==x]["CourseCode"].values[0])
        if st.button("Show Trend"):
            df_tr = course_trend(cid)
            if not df_tr.empty:
                chart = alt.Chart(df_tr).mark_line(point=True).encode(
                    x="Semester:O",
                    y=alt.Y("AvgMarks:Q", scale=alt.Scale(domain=[0,100])),
                    tooltip=["Semester", "AvgMarks"]
                )
                st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    st.subheader("Pass Rate by Department")
    df_pr = pass_rate_by_department()
    st.dataframe(df_pr)

    if not df_pr.empty:
        df_pr["PassPercent"] = df_pr["PassPercent"] / 100
    chart = alt.Chart(df_pr).mark_bar().encode(
        x="DepartmentName",
        y=alt.Y("PassPercent", axis=alt.Axis(format="%")),
        color="PassPercent"
    )
    st.altair_chart(chart, use_container_width=True)

# ---------------------
# MODIFY RECORDS
# ---------------------
elif page == "Modify Records":
    st.header("Add / Update / Delete Records")

    action = st.selectbox("Action", [
        "Add Student", "Update Student", "Delete Student",
        "Add Result", "Update Marks", "Delete Result",
        "Recompute Grades (Stored Proc)", "Update CourseStats (Cursor)"
    ])

    # ----------------- Add Student -----------------
    if action == "Add Student":
        st.subheader("Add Student")
        with st.form("add_stu"):
            roll = st.text_input("Roll No")
            name = st.text_input("Name")
            gender = st.selectbox("Gender", ["Male","Female","Other"])
            import datetime
            dob = st.date_input(
                "DOB",
                min_value=datetime.date(1980, 1, 1),
                max_value=datetime.date.today()
            )
            deps = list_departments()
            dept = st.selectbox("Department", deps["DepartmentID"],
                format_func=lambda x: deps[deps["DepartmentID"]==x]["DepartmentName"].values[0])
            batch = st.number_input("Batch Year", 2018, 2035, 2024)
            email = st.text_input("Email")
            if email and "@" not in email:
                st.warning("Invalid email format")
            phone = st.text_input("Phone")
            if st.form_submit_button("Add"):
                add_student(roll, name, gender, dob.isoformat(), int(dept), int(batch), email, phone)
                st.success("Student added.")
                time.sleep(1)
                st.rerun()

    # ----------------- Update Student -----------------
    elif action == "Update Student":
        sid = st.number_input("Student ID", 1)
        with st.form("upd_stu"):
            name = st.text_input("New Name")
            email = st.text_input("New Email")
            phone = st.text_input("New Phone")
            if st.form_submit_button("Update"):
                updates = {}
                if name: updates["Name"] = name
                if email: updates["Email"] = email
                if phone: updates["Phone"] = phone
                update_student(sid, **updates)
                st.success("Updated.")

    # ----------------- Delete Student -----------------
    elif action == "Delete Student":
        sid = int(st.number_input("Student ID", min_value=1, step=1, format="%d"))

        confirm = st.checkbox("I confirm deletion")
        if st.button("Delete") and confirm:
            delete_student(sid)
            st.success("Student deleted successfully!")
            st.cache_data.clear()
            st.rerun()

    # ----------------- Add Result -----------------
    elif action == "Add Result":
        with st.form("add_res"):
            sid = st.number_input("Student ID")
            cid = st.number_input("Course ID")
            eid = st.number_input("Exam ID")
            marks = st.number_input("Marks", 0.0, 100.0)
            if st.form_submit_button("Add"):
                add_result(int(sid), int(cid), int(eid), float(marks))
                st.success("Result added.")

    # ----------------- Update Marks -----------------
    elif action == "Update Marks":
        with st.form("upd_marks"):
            sid = st.number_input("Student ID")
            cid = st.number_input("Course ID")
            eid = st.number_input("Exam ID")
            marks = st.number_input("New Marks", 0.0, 100.0)
            if st.form_submit_button("Update"):
                update_marks(int(sid), int(cid), int(eid), float(marks))
                st.success("Marks updated.")

    # ----------------- Delete Result -----------------
    elif action == "Delete Result":
        rid = st.number_input("Result ID")
        if st.button("Delete"):
            from college_result_system import delete_result
            delete_result(int(rid))
            st.success("Result deleted.")

    # ----------------- Stored Procedure -----------------
    elif action == "Recompute Grades (Stored Proc)":
        if st.button("Run"):
            call_recompute_all_grades()
            st.success("Grades recomputed via Stored Procedure.")

    # ----------------- Cursor Procedure -----------------
    elif action == "Update CourseStats (Cursor)":
        if st.button("Run Cursor"):
            call_update_course_averages_cursor()
            st.success("CourseStats updated using Cursor.")
            st.markdown("### Updated CourseStats")
            st.dataframe(get_course_stats())

# ---------------------
# EXPORT & UTILITIES
# ---------------------
elif page == "Export & Utilities":
    st.header("Export & Utilities")

    # Export students
    if st.button("Export students (CSV)"):
        df = get_all_students()
        st.download_button("Download CSV", df_to_csv_bytes(df), file_name="students.csv")

    # Export subject averages
    if st.button("Export subject averages (Excel)"):
        df = subject_wise_average()
        st.download_button("Download Excel", df_to_excel_bytes(df), file_name="subject_averages.xlsx")

    st.markdown("---")
    st.subheader("CourseStats (Generated by Cursor)")
    st.dataframe(get_course_stats())

    st.download_button("Export CourseStats (CSV)",
        df_to_csv_bytes(get_course_stats()),
        file_name="coursestats.csv")

    st.download_button("Export CourseStats (Excel)",
        df_to_excel_bytes(get_course_stats()),
        file_name="coursestats.xlsx")

    st.markdown("---")
    st.subheader("Top Subjects Chart")
    df_sub = subject_wise_average()
    fig = plot_subject_bar(df_sub, top_n=10)
    if fig:
        st.pyplot(fig)

    st.markdown("---")
    st.json(quick_summary())

# ---------------------
# HELP
# ---------------------
elif page == "Help":
    st.header("Help & Viva Notes")
    st.markdown("""
### What to show in Viva:

1. **Database Schema**  
   Student, Course, Exam, Result  
   + Trigger (auto grade)  
   + Stored Procedure (RecomputeAllGrades)  
   + Cursor Procedure (UpdateCourseAveragesCursor)  
   + SQL Function (CalculateGPA)

2. **Live Use cases**  
   - Add / Update Students  
   - Add / Update Marks  
   - Stored Procedure run  
   - Cursor run  
   - CourseStats updates live  
   - GPA from SQL function

3. **Analytics**
   - Subject averages  
   - Trends  
   - Pass rate  
   - Toppers  

4. **Export Dashboard**
   CSV + Excel for all important datasets
""")
import streamlit as st
import pandas as pd
import json
import os

st.title("Student Analytics Dashboard")

# Load data
json_path = os.path.join(os.path.dirname(__file__), "..", "data", "student_english_results.json")
with open(json_path, "r") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Top students (A grade)
st.subheader("🏅 Top Students (Grade A)")
top_students = df[df["Grade"] == "A"].sort_values(by="Marks", ascending=False)
st.dataframe(top_students[["Name", "Marks", "Grade"]], use_container_width=True)

# Students needing improvement (Grade D or Marks < 60)
st.subheader("⚠️ Students Needing Improvement")
need_improve = df[(df["Grade"] == "D") | (df["Marks"] < 60)]
st.dataframe(need_improve[["Name", "Marks", "Grade"]], use_container_width=True)

# Attendance analytics (if available)
if "Attendance" in df.columns:
    st.subheader("📊 Attendance Overview")
    st.write(f"Average Attendance: {df['Attendance'].mean():.1f}%")
    st.dataframe(df.sort_values(by="Attendance")[["Name", "Attendance"]], use_container_width=True)

# General statistics
st.subheader("📈 General Statistics")
st.write(f"Average Marks: {df['Marks'].mean():.2f}")
st.write(f"Grade Distribution:")
st.bar_chart(df["Grade"].value_counts())

# Weaknesses and Suggestions summary
st.subheader("🔍 Common Weaknesses & Suggestions")
st.write("**Top Weaknesses:**")
st.write(df["Weakness"].value_counts().head(5))
st.write("**Top Suggestions:**")
st.write(df["Suggestion"].value_counts().head(5))

import os
import json
from helper_functions import llm

# Load student results JSON from file
filepath = './data/student_english_results.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_result = json.loads(json_string)


def analyze_student(student: dict) -> str:
    delimiter = "####"

    system_message = f"""
You are an AI assistant designed to support tutors by analyzing student performance data. 
The student's performance record will be enclosed in the pair of {delimiter}.

Each student entry is a dictionary containing fields like:
- Name
- Grade
- Marks
- Weakness
- Suggestion

Your task is to:
1. Understand the student's current academic standing based on the provided data.
2. Identify key weaknesses and potential areas of concern.
3. Recommend actionable strategies or interventions the tutor can apply to help the student improve.
4. Keep your advice detailed, empathetic, and practical.

Respond with a **single string of advice** tailored to the tutor for this specific student. 
Avoid repeating the input fields word-for-word — interpret the data to give useful insights.

Example format of student data:
{{
  "Name": "Zulfa Noor",
  "Grade": "C",
  "Marks": 60,
  "Weakness": "Weak in oral presentations",
  "Suggestion": "Practice presenting to family"
}}

Only respond with a recommendation string, without any additional tags, formatting, or delimiters.
"""

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{json.dumps(student)}{delimiter}"}
    ]

    response = llm.get_completion_by_messages(messages)
    return response.strip()


def generate_final_response_to_tutor(advice_list: list) -> str:
    response = "Here are the recommendations for your students:\n\n"
    for entry in advice_list:
        response += f"Student: {entry['Name']}\nAdvice: {entry['Advice']}\n\n"
    return response.strip()


def process_user_message(user_input: str):
    student_data = dict_of_result
    print("Loaded student data successfully.")

    # Identify which student the user is asking about
    student = find_student_in_message(user_input, student_data)

    if student:
        # Analyze that student's performance
        advice = analyze_student(student)
        reply = f"Student: {student['Name']}\nAdvice: {advice}"
        return reply, [{"Name": student["Name"], "Advice": advice}]
    else:
        # If not a student-specific query, treat as general teaching/education question
        teaching_system_message = f"""
You are an expert AI teaching assistant and summary on the student result {dict_of_result}. Answer the user's question with helpful, practical, and evidence-based advice for teachers, tutors, or educators. Be clear, concise, and friendly. If the question is about pedagogy, classroom management, assessment, student motivation, or any teaching topic, provide your best guidance.
"""
        messages = [
            {'role': 'system', 'content': teaching_system_message},
            {'role': 'user', 'content': user_input}
        ]
        response = llm.get_completion_by_messages(messages)
        return response.strip(), []


def find_student_in_message(user_message: str, all_students: list[dict]) -> dict:
    for student in all_students:
        name = student.get("Name", "").lower()
        if name in user_message.lower():
            return student
    return None



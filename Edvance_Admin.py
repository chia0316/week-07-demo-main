# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Edvance Admin Dashboard",
    page_icon=":guardsman:",
    initial_sidebar_state="expanded",
)



# Sidebar navigation with logo at the top, settings, and sample chat sessions
with st.sidebar:
    st.image("logo.png", width=90)
    # Sample chat session quick prompts

# Check if the password is correct.
if not check_password():
    st.stop()
# endregion <--------- Streamlit App Configuration --------->

st.title("Edvance LLM Tutor Assistant")

# ---- State init
if "chat_history" not in st.session_state:
    # Add sample chat history for a ChatGPT-like experience
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Hello! I'm Edvance, your AI tutor assistant. How can I help you today?"},
        {"role": "user", "content": "Can you show me the top students in my class?"},
        {"role": "assistant", "content": "Sure! Here are the top students based on their marks and grades. (You can upload your student results for more personalized analytics.)"},
        {"role": "user", "content": "What advice do you have for Ben Tan?"},
        {"role": "assistant", "content": "Ben Tan has a C grade and limited vocabulary. Encourage him to read more English books and articles, and provide vocabulary-building exercises."},
    ]
if "last_course_details" not in st.session_state:
    st.session_state["last_course_details"] = None

# ---- Layout containers (history above, input below)
history_container = st.container()
input_container = st.container()

# ---- Input form (kept visually at the bottom)
with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_prompt = st.text_area("Type your message...", height=80, key="chat_input")
        submitted = st.form_submit_button("Send")

    if submitted and user_prompt.strip():
        # Append user message first
        st.session_state["chat_history"].append({"role": "user", "content": user_prompt})

        # Call your AI logic immediately and handle errors
        try:
            with st.spinner("Thinking..."):
                result = process_user_message(user_prompt)
        except Exception as e:
            # Surface errors in UI and add an assistant message describing the error
            st.exception(e)
            ai_text = "Sorry, I hit an error while generating a reply. I've shown the details above."
            st.session_state["chat_history"].append({"role": "assistant", "content": ai_text})
            st.session_state["last_course_details"] = None
        else:
            # Support either a tuple (response, details) or just a string response
            if isinstance(result, tuple) and len(result) >= 1:
                response = result[0]
                course_details = result[1] if len(result) > 1 else None
            else:
                response, course_details = str(result), None

            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            st.session_state["last_course_details"] = course_details


# ---- Render chat AFTER processing so latest messages appear immediately
import streamlit.components.v1 as components
with history_container:
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="background:#e6f0fa;padding:0.7em 1em;border-radius:1em;'
                f'margin-bottom:0.5em;max-width:70%;margin-left:auto;text-align:right;">'
                f'<b>You:</b> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background:#f4f4f4;padding:0.7em 1em;border-radius:1em;'
                f'margin-bottom:0.5em;max-width:70%;margin-right:auto;text-align:left;">'
                f'<b>Assistant:</b> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    # Course details shown right below the chat (if any)
    course_details = st.session_state.get("last_course_details", None)
    if course_details:
        st.divider()
        st.write("**Student Details:**")
        try:
            df = pd.DataFrame(course_details)
            st.dataframe(df)
        except Exception:
            # Fall back gracefully if course_details isn't tabular
            st.write(course_details)

    # Add an anchor at the bottom and auto-scroll to it
    components.html("""
        <script>
        var anchor = document.getElementById('bottom-anchor');
        if(anchor){anchor.scrollIntoView({behavior: 'smooth'});}
        </script>
        <div id='bottom-anchor'></div>
    """, height=0)

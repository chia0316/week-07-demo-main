import streamlit as st
import random
import hmac

# """
# This file contains the common components used in the Streamlit App.
# This includes the sidebar, the title, the footer, and the password check.
# """


def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            hmac.compare_digest(st.session_state.get("password", ""), st.secrets["password"]) and
            hmac.compare_digest(st.session_state.get("username", ""), st.secrets.get("username", "admin"))
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Beautified login form
    st.markdown("""
        <style>
        .login-card {
            background-color: #f8f9fa;
            padding: 2.5rem 2rem 2rem 2rem;
            border-radius: 1.2rem;
            box-shadow: 0 4px 24px 0 rgba(0,0,0,0.10);
            max-width: 350px;
            margin: 3rem auto 1rem auto;
        }
        .login-title {
            text-align: center;
            font-size: 1.6rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('''<div class="login-card">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <span style="font-size:2.2rem;font-weight:700;color:#2c3e50;margin-bottom:1.2rem;letter-spacing:2px;">Edvance</span>
            </div>''', unsafe_allow_html=True)
        st.markdown('<div class="login-title">User Login</div>', unsafe_allow_html=True)
        st.text_input("Username", key="username", placeholder="Enter your username")
        st.text_input("Password", type="password", on_change=password_entered, key="password", placeholder="Enter your password")
        st.markdown('</div>', unsafe_allow_html=True)

    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Username or Password incorrect")
    return False

import streamlit as st
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

def check_password():
    """
    Returns `True` if the user has supplied the correct password.
    Displays a login form if they haven't.
    """
    
    # Get hash from environment
    stored_hash = os.getenv("APP_PASSWORD")
    
    # If no password is set, bypass security (default to open)
    if not stored_hash:
        return True

    # Return True if password has already been checked and is correct
    if st.session_state.get("password_correct", False):
        return True

    # Login page styling
    st.markdown("""
    <style>
        [data-testid="stForm"] {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #F63366;
            box-shadow: 0 0 30px rgba(246, 51, 102, 0.15);
        }
        [data-testid="stForm"] button[type="submit"] {
            background: linear-gradient(90deg, #F63366 0%, #FF6B6B 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Simple, clean login UI
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.title("🔐 Secure Login")
        st.write("Welcome back! Please enter your application password to access your Habit Tracker.")
        
        with st.form("login_form"):
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login 🚀", use_container_width=True)
            
            if submit:
                try:
                    # Verify bcrypt hash
                    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                        st.session_state["password_correct"] = True
                        st.rerun()
                    else:
                        st.session_state["password_correct"] = False
                except Exception as e:
                    st.error(f"Error verifying password: {e}")
                    st.session_state["password_correct"] = False
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Password incorrect. Please try again.")
            
        st.divider()
        

    return False

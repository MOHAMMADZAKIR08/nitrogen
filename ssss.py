import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import os

PASSWORD_FILE = "password.txt"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_password_hash():
    if not os.path.exists(PASSWORD_FILE):
        # Set a default password if none exists
        with open(PASSWORD_FILE, "w") as f:
            f.write(hash_password("admin"))
        return hash_password("admin")
    with open(PASSWORD_FILE, "r") as f:
        return f.read().strip()


def save_password_hash(new_hash: str):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new_hash)

def login():
    st.title("Login")
    password = st.text_input("Enter password:", type="password")
    if st.button("Login"):
        stored_hash = load_password_hash()
        if hash_password(password) == stored_hash:
            st.session_state["authenticated"] = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Incorrect password.")


def reset_password():
    st.subheader("Reset Password")
    current = st.text_input("Current password", type="password")
    new = st.text_input("New password", type="password")
    confirm = st.text_input("Confirm new password", type="password")
    if st.button("Change Password"):
        stored_hash = load_password_hash()
        if hash_password(current) != stored_hash:
            st.error("Current password is incorrect.")
        elif new != confirm:
            st.error("New passwords do not match.")
        elif not new:
            st.error("New password cannot be empty.")
        else:
            save_password_hash(hash_password(new))
            st.success("Password changed successfully. Please log in again.")
            st.session_state["authenticated"] = False
            st.experimental_rerun()


def main_app():
    st.title("Your App")
    st.sidebar.button("Reset Password", on_click=lambda: st.session_state.update({"show_reset": True}))
    if st.session_state.get("show_reset"):
        reset_password()
        if st.button("Back to App"):
            st.session_state["show_reset"] = False
            st.experimental_rerun()
    else:
        dashboard_page()  # Your main dashboard logic here

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "show_reset" not in st.session_state:
    st.session_state["show_reset"] = False

if not st.session_state["authenticated"]:
    login()
else:
    main_app()

# ...rest of your dashboard_page and other logic below remains unchanged

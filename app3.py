import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Title for the landing page
st.title("Welcome to StyleMe!")

# Initialize session state to store users if it doesn't already exist
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'account_created' not in st.session_state:
    st.session_state['account_created'] = False  # Track account creation status

# Email credentials (replace with your actual email server credentials)
EMAIL_ADDRESS = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"

# Global red background styling
st.markdown(
    """
    <style>
    body {
        background-color: #FF0000;
    }
    </style>
    """, unsafe_allow_html=True
)

# Function to create an account
def create_account():
    st.subheader("Create an Account")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    email = st.text_input("Enter Email Address")

    if st.button("Sign Up"):
        if new_username and new_password and email:
            if new_username in st.session_state['users']:
                st.warning("Username already exists. Please choose a different one.")
            else:
                st.session_state['users'][new_username] = {
                    "password": new_password,
                    "email": email
                }
                st.session_state['account_created'] = True
                st.balloons()
        else:
            st.warning("Please enter a username, password, and email address.")

# Function for login
def login():
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if username and password match stored credentials
        if username in st.session_state['users'] and st.session_state['users'][username]['password'] == password:
            st.success("✅ Success")
        else:
            st.error("❌ Incorrect username or password")

    # Forgot username/password option
    if st.button("Forgot Username/Password?"):
        forgot_password()

# Function for forgot username/password page
def forgot_password():
    st.subheader("Recover Account Information")
    recovery_email = st.text_input("Enter your account email to recover your username/password information")

    if st.button("Send Recovery Email"):
        user_found = None
        for username, user_info in st.session_state['users'].items():
            if user_info['email'] == recovery_email:
                user_found = (username, user_info['password'])
                break

        if user_found:
            send_recovery_email(recovery_email, user_found[0], user_found[1])
            st.success("Recovery email sent! Check your inbox.")
            st.info("An email with username/password recovery instructions has been sent to the email you provided.")
        else:
            st.error("No account found with that email address.")

# Function to send recovery email
def send_recovery_email(email, username, password):
    subject = "Your StyleMe Account Recovery Information"
    body = f"Here are your account details:\n\nUsername: {username}\nPassword: {password}"
    msg = MIMEText(body)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject

    # Connect to the email server and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())

# Main landing page
st.subheader("What would you like to do?")
choice = st.radio("", ("Create an Account", "Login to an Account"))

if choice == "Create an Account":
    create_account()
    # After account creation, show login fields on the same page
    if st.session_state['account_created']:
        st.success("Account created successfully! Please log in below.")
        login()

elif choice == "Login to an Account":
    login()

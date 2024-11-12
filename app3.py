import streamlit as st

# Set the title for the landing page
st.title("Welcome to StyleMe")

# Initialize session state to store users if it doesn't already exist
if 'users' not in st.session_state:
    st.session_state['users'] = {}

# Define main function for landing page
def main():
    # Landing page options
    choice = st.radio("What would you like to do?", ("Create an Account", "Login to an Account"))

    # Direct user based on their choice
    if choice == "Create an Account":
        create_account()
    elif choice == "Login to an Account":
        login()

# Function to create an account
def create_account():
    st.subheader("Create an Account")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        if new_username and new_password:
            if new_username in st.session_state['users']:
                st.warning("Username already exists. Please choose a different one.")
            else:
                st.session_state['users'][new_username] = new_password
                st.success("Account created successfully! You can now log in.")
        else:
            st.warning("Please enter both a username and password.")

# Function for login
def login():
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if username and password match stored credentials
        if username in st.session_state['users'] and st.session_state['users'][username] == password:
            st.success("✅ Success")
        else:
            st.error("❌ Incorrect username or password")

# Run the main function
if __name__ == "__main__":
    main()

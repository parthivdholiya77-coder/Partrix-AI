import streamlit as st
from backend.auth.service import AuthService


def show_auth_page():
    st.title("🤖 Partrix AI")

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Login",
            key="nav_login",
            use_container_width=True,
        ):
            st.session_state.auth_page = "login"
            st.rerun()

    with col2:
        if st.button(
            "Sign Up",
            key="nav_signup",
            use_container_width=True,
        ):
            st.session_state.auth_page = "signup"
            st.rerun()

    st.divider()

    if st.session_state.auth_page == "login":
        show_login()
    else:
        show_signup()


def show_login():
    st.subheader("Login")

    email = st.text_input(
        "Email",
        key="login_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
    )

    if st.button(
        "Login",
        key="login_btn",
        use_container_width=True,
    ):
        success, result = AuthService.login(email, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.user = result

            st.success(f"Welcome {result['username']}!")
            st.rerun()

        else:
            st.error(result)


def show_signup():
    st.subheader("Create Account")

    username = st.text_input(
        "Username",
        key="signup_username",
    )

    email = st.text_input(
        "Email",
        key="signup_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="signup_password",
    )

    if st.button(
        "Create Account",
        key="signup_btn",
        use_container_width=True,
    ):
        success, result = AuthService.signup(
            username,
            email,
            password,
        )

        if success:
            st.session_state.pop("signup_username", None)
            st.session_state.pop("signup_email", None)
            st.session_state.pop("signup_password", None)
            st.success("Account created successfully!")
            st.info("Please login with your new account.")

            st.session_state.auth_page = "login"

            

            st.rerun()

        else:
            st.error(result)
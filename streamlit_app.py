import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Uni-One Streamlit Demo")

if "token" not in st.session_state:
    st.session_state.token = None

menu = st.sidebar.radio("Navigation", ["Register", "Login", "View Posts", "Create Post"])

if menu == "Register":
    st.header("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        r = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
        if r.status_code == 200:
            st.success("Registered successfully")
        else:
            st.error(r.text)

elif menu == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        r = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.success("Logged in")
        else:
            st.error(r.text)

elif menu == "View Posts":
    st.header("Recent Posts")
    r = requests.get(f"{BASE_URL}/posts")
    if r.status_code == 200:
        posts = r.json()
        for p in posts:
            st.write(f"**{p['author']}**: {p['content']}")
    else:
        st.error("Failed to load posts")

elif menu == "Create Post":
    if not st.session_state.token:
        st.warning("You must log in first")
    else:
        st.header("New Post")
        content = st.text_area("Content")
        if st.button("Submit"):
            r = requests.post(
                f"{BASE_URL}/posts",
                params={"content": content},
                headers={"Authorization": f"Bearer {st.session_state.token}"},
            )
            if r.status_code == 200:
                st.success("Post created")
            else:
                st.error(r.text)

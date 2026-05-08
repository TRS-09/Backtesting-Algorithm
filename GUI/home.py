import streamlit as st

def home_page():
    st.title("Home Page")

    st.write("Welcome to the app!")

    if st.button("Click me"):
        st.success("Button was clicked!")
        st.balloons()

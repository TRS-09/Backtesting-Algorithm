import streamlit as st

def settings_page():
    st.title("Settings")

    username = st.text_input("Enter your name")
    number = st.slider("Pick a number", 0, 100)

    st.write("Name:", username)
    st.write("Number:", number)

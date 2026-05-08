import streamlit as st
from GUI.home import home_page
from GUI.settings import settings_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Settings","AUDIO"])

    if page == "Home":
        home_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
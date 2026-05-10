import streamlit as st

def home_page():

    c1, c2, c3 = st.columns([1,2,1])

    with c2:
        st.markdown("<div style='text-align : center ; font-size : 70px'>Welcome</div>",unsafe_allow_html=True)

    with c2:
        st.markdown("<div style = 'text-align : center'>Ready to backtest!</div>",unsafe_allow_html=True)

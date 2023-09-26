import streamlit as st

from predict_page import show_predict_page
from explore_page import show_explore_page

options = ("Predecir", "Explorar")
page = st.sidebar.selectbox("Elija una opción", options)

if page =="Predecir":
    show_predict_page()
else:
    show_explore_page()

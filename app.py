import streamlit as st

# Establece el estilo de la barra lateral
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

from predict_page import show_predict_page
from explore_page import show_explore_page

options = ("Predecir", "Explorar")
page = st.sidebar.selectbox("Elija una opción", options)

if page == "Predecir":
    show_predict_page()
else:
    show_explore_page()

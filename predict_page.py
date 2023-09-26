import streamlit as st
import pickle  # To load the data
import numpy as np

# Se crea la función para cargar el modelo entrenado
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


def show_predict_page():
    st.title("Calculadora de Salario (Desarrollo de Software)")

    # Añadir un contenedor para centrar el formulario
    form = st.form(key='prediction_form')
    col1, col2 = form.columns(2)

    with col1:
        countries = (
            "United States of America",
            "Germany",
            "United Kingdom of Great Britain and Northern Ireland",
            "Canada",
            "India",
            "France",
            "Netherlands",
            "Australia",
            "Brazil",
            "Spain",
            "Sweden",
            "Italy",
            "Poland",
            "Switzerland",
            "Denmark",
            "Norway",
            "Israel",
        )

        country = st.selectbox("País", countries)

    with col2:
        education = (
            "Less than a Bachelors",
            "Bachelor’s degree",
            "Master’s degree",
            "Post grad",
        )

        education = st.selectbox("Educación", education)

    experience = st.slider("Años de Experiencia", 0, 50, 3)
    ok = form.form_submit_button("Calcular Salario")

    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"El salario estimado es: ${salary[0]:,.02f}")

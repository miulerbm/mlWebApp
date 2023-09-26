import streamlit as st
import pickle # To load the data
import numpy as np


# Se crea la función para cargar el modelo entrenado
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

# Accedemos a los diferentes elementos del archivo
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Herramienta de Predicción de Salario (Software Development)")

    st.write("""### Introduzca sus datos""")

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



    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    # Las tuplas definidas arriba se empleand como las opciones del
    # selectbox. Tanto para country como para education
    # El valor seleccionado en la interfaz será cargado a la variable definida:
    country = st.selectbox("País", countries)
    education = st.selectbox("Educación", education)

    # Ahora, para los años de experiencia:
    experience = st.slider("Años de Experiencia", 0, 50, 3)
    # Límite inferior, lím superior y valor default

    # Ahora, para el botón de Calcular Salario:
    ok = st.button("Predecir mi salario")

    # Si es que damos click a "ok", será true:
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"El salario será aproximadamente: ${salary[0]:,.02f}")

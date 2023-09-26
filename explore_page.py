import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache # Para que se ejecute una vez y la siguiente esté en caché y no deba
# ejecutarse de nuevo:

def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Data de otros Desarrolladores")

    st.write(
        """
        ### Stack Overflow Developer Survey 2023
        """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=None, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    # Para tener una leyenda legible
    legend_labels = data.index
    plt.legend(legend_labels, title="Countries", loc="center left", bbox_to_anchor=(1, 0.5))

    st.write("""### Cantidad de Datos de Diversos Países""")
    st.pyplot(fig1)

    st.write(
        """
    #### Salario promedio por País
        """
    )

    # Se agrupan los Salarios por País
    data = df.groupby(["Country"])["Salary"].mean()

    st.bar_chart(data)


    st.write(
        """
        #### Salario Medio por Años de Experiencia
        """
    )


    data = df.groupby(["YearsCodePro"])["Salary"].mean()
    st.line_chart(data)
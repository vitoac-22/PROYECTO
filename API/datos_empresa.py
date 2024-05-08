import pandas as pd
import os
import streamlit as st


def datos_empresa():
    # Ruta completa al archivo CSV
    ruta_archivo = r"BD\symbols_valid_meta.csv"

    # Cargar el archivo CSV en un DataFrame
    nombre_empresa = pd.read_csv(ruta_archivo)

    # Selección de la empresa
    # empresa = list(nombre_empresa["Security Name"].unique())
    simbolo = list(nombre_empresa["NASDAQ Symbol"].unique())
    return simbolo


# # Widget para escoger a la empresa
# inicial_empresa = st.selectbox("Escoga las iniciales de la empresa", simbolo)

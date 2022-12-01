import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# Sidbar menu
st.sidebar.title("Menu")

page_selectbox = st.sidebar.selectbox("Selecione a página", ["Home", "Suavização Exponencial", "Modelos", "Comparativo"])

st.sidebar.write("By Natã Santana, Rafhael Martins, Victor Resende")
st.sidebar.write("01 de Dezembro de 2022")

def page_home():
    st.title('Análise de Séries Temporais')
    st.header("Produção de Soja no Brasil")
    st.write("A base de dados é uma série histórica da produção de soja (em toneladas de grãos) por ano, desde 1990 até 2016 no Brasil. Em seu histórico, a registro de uma produção mínima de 14.937.806 milhões de toneladas de grãos e uma produção máxima de 97.464.936 milhões de toneladas de grãos, com uma média anual de produção de 48.287.590 milhões de toneladas de grãos por ano.")

    st.subheader("Dataset :floppy_disk:")
    df = pd.read_csv("dados/producao_soja_st.txt", sep=';')

    if st.checkbox("Mostrar o dataset"):
        st.dataframe(df)  

    st.subheader("Correlograma da série")
    st.line_chart(df, x="ANO", y="PRODUCAO")

    st.subheader("Caracterísitcas da série temporal")
    st.markdown("""
    - **start (início):** Inicia no ano de 1990.
    - **end (fim):** Termina em no ano de 2016.
    - **class (classe):** Trata-se de uma base de Série Temporal (Time Series).
    """)

if page_selectbox == "Home":
    page_home()

elif page_selectbox == "Suavização Exponencial":
    st.title("Modelos de Suavização Exponencial")

elif page_selectbox == "Modelos":
    st.title("Modelos para Série Temporais")

elif page_selectbox == "Comparativo":
    st.title("Comparativo Produção de Soja X PIB")


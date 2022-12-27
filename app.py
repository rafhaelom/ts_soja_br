########## PRODUÇÃO DE SOJA NO BRASIL ########## 
# Disciplina: Séries Temporais.
# Professor: Suélio Alves de Moura.
# Autores: Natã Ferreira Santana
#          Rafhael de Oliveira Martins
#          Victor Augusto Souza Resende
           
# Links utilizados:
# SOJA: https://seriesestatisticas.ibge.gov.br/series.aspx?no=1&op=0&vcodigo=PA3&t=lavoura-temporaria-quantidade-produzida

import streamlit as st

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.stattools import adfuller # importar o teste ADF
#from statsmodels.tsa.arima import ARIMA
import statsmodels.api as sm

# Sidbar menu
st.sidebar.title("Menu")

page_selectbox = st.sidebar.selectbox("Selecione a página", ["Home", "Suavização Exponencial", "Modelos", "Comparativo"])

st.sidebar.write("By Natã Santana, Rafhael Martins, Victor Resende")
st.sidebar.write("01 de Dezembro de 2022")

df = pd.read_csv("dados/producao_soja_st.txt", sep=';')

dados = df["PRODUCAO"].values
index = pd.date_range(start="1990", end="2017", freq="A")
soja_ts = pd.Series(dados, index)

def page_home():
    st.title('Análise de Séries Temporais')
    st.header("Produção de Soja no Brasil")
    st.markdown("""<p align='justify'>A base de dados é uma série histórica da produção de soja (em toneladas de grãos) por ano, desde 1990 até 2016 no Brasil. Em seu histórico, a registro de uma produção mínima de 14.937.806 milhões de toneladas de grãos e uma produção máxima de 97.464.936 milhões de toneladas de grãos, com uma média anual de produção de 48.287.590 milhões de toneladas de grãos por ano.<p align='justify'>""", unsafe_allow_html=True)

    st.subheader("Dataset :floppy_disk:")
    if st.checkbox("Mostrar o dataset"):
        st.dataframe(soja_ts)

    st.subheader("Caracterísitcas da série temporal")
    st.markdown("""
    - **start (início):** Inicia no ano de 1990.
    - **end (fim):** Termina em no ano de 2016.
    - **class (classe):** Trata-se de uma base de Série Temporal (Time Series).
    """) 

    st.subheader("Correlograma da série")
    #st.line_chart(df, x="ANO", y="PRODUCAO")

    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(data=soja_ts)
    plt.title("PRODUÇÃO DE SOJA POR ANO NO BRASIL")
    plt.xlabel("ANO") 
    plt.ylabel("PRODUCAO")
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig)
    plt.clf()

    st.subheader("Componentes da série temporal")
    st.markdown("""
    - **Tendência:** Os dados possuem uma forte tendência de aumento.
    - **Sazonalidade:** Os dados não possuem a componente sazonal, não obedecendo padrões com durações fixas.
    - **Ciclo:** A série possui um componente variando em ciclos, porém sem duração fixa.
    """)

    st.subheader("ACF e PACF")
    lag_acf = acf(soja_ts)
    lag_pacf = pacf(soja_ts)

    # plotar ACF e PACF
    fig = plt.figure(figsize=(10, 4))
    plt.plot(lag_acf)
    plt.axhline(y=-1.96 / (np.sqrt((len(soja_ts) - 1))), linestyle='--', color='gray', linewidth=0.7)
    plt.axhline(y=0, linestyle='--', color='gray', linewidth=0.7)
    plt.axhline(y=1.96 / (np.sqrt((len(soja_ts) - 1))), linestyle='--', color='gray', linewidth=0.7)
    plt.title("ACF (Autocorrelação)")
    st.pyplot(fig)
    plt.clf()

    fig = plt.figure(figsize=(10, 4))
    plt.plot(lag_pacf)
    plt.axhline(y=-1.96 / (np.sqrt((len(soja_ts) - 1))), linestyle='--', color='gray', linewidth=0.7)
    plt.axhline(y=0, linestyle='--', color='gray', linewidth=0.7)
    plt.axhline(y=1.96 / (np.sqrt((len(soja_ts) - 1))), linestyle='--', color='gray', linewidth=0.7)
    plt.title("PACF (Autocorrelação Parcial)")
    st.pyplot(fig)
    plt.clf()

def page_s_e():
    st.title("Modelos de Suavização Exponencial")
    model_select = st.selectbox("Selecione um modelo", ["Suavização Exponencial Simple (SES)", "Suavização Exponencial de Holt (SEH)"]) #, "Comparativo dos Modelos"

    # Tabela de resultados dos modelos.
    results = pd.DataFrame(
        index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$l_0$", "$b_0$", "SSE"],
        columns=["SES", "Holt's"],
        )

    params = [
        "smoothing_level",
        "smoothing_trend",
        "damping_trend",
        "initial_level",
        "initial_trend",
        ]

    # Gerando as previsões
    fit1 = SimpleExpSmoothing(soja_ts, initialization_method="heuristic").fit(smoothing_level=0.2, optimized=False)
    model_ses = fit1.forecast(5).rename("Simple Exponential Smoothing")

    results["SES"] = [fit1.params[p] for p in params] + [fit1.sse]

    # Gerando as previsões
    fit2 = Holt(soja_ts, initialization_method="estimated").fit(smoothing_level=0.8, smoothing_trend=0.2, optimized=False)
    model_seh = fit2.forecast(5).rename("Holt's linear trend")

    results["Holt's"] = [fit2.params[p] for p in params] + [fit2.sse]

    # Tabela previsões dos modelos.
    predict_models = pd.DataFrame(
        columns=["SES", "SEH"],
        )

    predict_models["SES"] = model_ses
    predict_models["SEH"] = model_seh

    #Treinando o modelos de suavização.
    if model_select == "Suavização Exponencial Simple (SES)":
        st.header("Suavização Exponencial Simple (SES)")

        st.subheader("Previsão:")
        st.markdown("""<p align='justify'>Previsão realizada para os próximos 5 anos.<p align='justify'>""", unsafe_allow_html=True)
        if st.checkbox("Mostrar o previsão"):
            st.write(model_ses)

        fig = plt.figure(figsize=(10, 4))
        sns.lineplot(data=soja_ts)
        sns.lineplot(data=model_ses)
        plt.title("PRODUÇÃO DE SOJA POR ANO NO BRASIL")
        plt.xlabel("ANO") 
        plt.ylabel("PRODUCAO")
        plt.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)
        plt.clf()

        st.dataframe(results["SES"])

    elif model_select == "Suavização Exponencial de Holt (SEH)":
        st.header("Suavização Exponencial de Holt (SEH)")
        
        st.subheader("Previsão:")
        st.markdown("""<p align='justify'>Previsão realizada para os próximos 5 anos.<p align='justify'>""", unsafe_allow_html=True)
        if st.checkbox("Mostrar o previsão"):
            st.write(model_seh)

        fig = plt.figure(figsize=(10, 4))
        sns.lineplot(data=soja_ts)
        sns.lineplot(data=model_seh)
        plt.title("PRODUÇÃO DE SOJA POR ANO NO BRASIL")
        plt.xlabel("ANO") 
        plt.ylabel("PRODUCAO")
        plt.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)
        plt.clf()

        st.dataframe(results["Holt's"])

    # elif model_select == "Comparativo dos Modelos":
    #     fig = plt.figure(figsize=(10, 4))
    #     sns.lineplot(data=soja_ts)
    #     sns.lineplot(data=model_ses, hue="SES")
    #     sns.lineplot(data=model_seh)
    #     plt.title("PRODUÇÃO DE SOJA POR ANO NO BRASIL")
    #     plt.xlabel("ANO") 
    #     plt.ylabel("PRODUCAO")
    #     plt.ticklabel_format(style='plain', axis='y')
    #     st.pyplot(fig)
    #     plt.clf()

    #     st.dataframe(results)

def page_models():
    st.title("Modelos para Série Temporais")

    # AR
    model_AR = sm.tsa.arima.ARIMA(soja_ts, order=(1,0,0))
    result_AR = model_AR.fit()

    # MA
    model_MA = sm.tsa.arima.ARIMA(soja_ts, order=(0,0,1))
    result_MA = model_MA.fit()

    # ARMA
    model_ARMA = sm.tsa.arima.ARIMA(soja_ts, order=(1,0,1))
    result_ARMA = model_ARMA.fit()

    # ARIMA
    model_ARIMA = sm.tsa.arima.ARIMA(soja_ts, order=(1,1,1))
    result_ARIMA = model_ARIMA.fit()

    model_select_arima = st.selectbox("Selecione um modelo", ["AR", "MA", "ARMA", "ARIMA"])

    if model_select_arima == "AR":
        st.write(result_AR.summary())
    elif model_select_arima == "MA":
        st.write(result_MA.summary())
    elif model_select_arima == "ARMA":
        st.write(result_ARMA.summary())
    elif model_select_arima == "ARIMA":
        st.write(result_ARIMA.summary())

def page_comparative():
    st.title("Comparativo Produção de Soja X PIB")

if page_selectbox == "Home":
    page_home()

elif page_selectbox == "Suavização Exponencial":
    page_s_e()

elif page_selectbox == "Modelos":
    page_models()

elif page_selectbox == "Comparativo":
    page_comparative()


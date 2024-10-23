import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

# Função para carregar dados
def carregar_dados(file):
    df = pd.read_csv(file, sep=';')
    return df

# Função para gerar gráficos
def gerar_graficos(df):
    st.subheader("Distribuição por Região")
    fig = px.pie(df, names='Região', title="Distribuição por Região")
    st.plotly_chart(fig)

    st.subheader("Distribuição por Sexo")
    fig = px.bar(df, x='Sexo', title="Distribuição por Sexo")
    st.plotly_chart(fig)

    st.subheader("Distribuição por Faixa Etária")
    fig = px.histogram(df, x='Faixa Etária', title="Distribuição por Faixa Etária")
    st.plotly_chart(fig)

    st.subheader("Distribuição por UF")
    fig = px.bar(df, x='UF', title="Distribuição por Estado (UF)")
    st.plotly_chart(fig)

    st.subheader("Situação das Reclamações")
    fig = px.pie(df, names='Situação', title="Situação das Reclamações")
    st.plotly_chart(fig)

# Função para gerar mapa
def gerar_mapa(df):
    st.subheader("Mapa de Reclamações por Cidade")
    
    # Aqui precisaremos de um shapefile ou base para mapear as cidades/regiões
    # No exemplo abaixo, estou considerando o uso de geopy ou uma base customizada de cidades
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))  # Exemplo, se tivermos coordenadas
    fig = px.scatter_geo(df, locations='Cidade', locationmode='country names', hover_name='Cidade', title="Reclamações por Cidade")
    st.plotly_chart(fig)

# Interface Streamlit
st.title("Análise de Reclamações")

# Upload de arquivo CSV
file = st.file_uploader("Envie o arquivo CSV", type=["csv"])

if file is not None:
    # Carregar dados
    df = carregar_dados(file)
    
    # Mostrar os primeiros registros
    st.write("Visualização da Amostra de Dados:")
    st.write(df.head())
    
    # Gerar gráficos
    gerar_graficos(df)
    
    # Gerar mapa
    if st.checkbox("Mostrar Mapa de Reclamações"):
        gerar_mapa(df)

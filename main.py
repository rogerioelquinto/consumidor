import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados
def carregar_dados(file):
    df = pd.read_csv(file, sep=';')
    return df

# Função para gerar gráficos
def gerar_graficos(df):
    # Substituir os rótulos das regiões
    df['Região'] = df['Região'].replace({
        'N': 'Norte',
        'S': 'Sul',
        'NE': 'Nordeste',
        'CO': 'Centro-Oeste',
        'SE': 'Sudeste'
    })
    
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

# Função para exibir a tabela com paginação
def exibir_tabela(df):
    st.write("Visualização da Amostra de Dados:")
    n = st.number_input('Número de registros por página', min_value=5, max_value=100, value=10)
    page = st.number_input('Página', min_value=1, max_value=(len(df) // n) + 1)
    start = (page - 1) * n
    end = start + n
    st.write(df.iloc[start:end])

# Interface Streamlit
st.title("Análise de Reclamações")

# Upload de arquivo CSV
file = st.file_uploader("Envie o arquivo CSV", type=["csv"])

if file is not None:
    # Carregar dados
    df = carregar_dados(file)
    
    # Mostrar os primeiros registros com paginação
    exibir_tabela(df)
    
    # Gerar gráficos
    gerar_graficos(df)

import pandas as pd
import streamlit as st
import math
import plotly.express as px

# Função para paginar o DataFrame
def paginar_dataframe(df, pagina_atual, linhas_por_pagina):
    total_paginas = math.ceil(len(df) / linhas_por_pagina)
    inicio = pagina_atual * linhas_por_pagina
    fim = inicio + linhas_por_pagina
    return df.iloc[inicio:fim], total_paginas

# Função para mostrar a tabela paginada
def mostrar_tabela_paginada(df):
    linhas_por_pagina = 10
    pagina_atual = st.sidebar.number_input("Selecione a página", min_value=1, max_value=(len(df) // linhas_por_pagina) + 1, step=1) - 1
    df_paginado, total_paginas = paginar_dataframe(df, pagina_atual, linhas_por_pagina)
    st.dataframe(df_paginado)
    st.sidebar.write(f"Página {pagina_atual + 1} de {total_paginas}")

# Função para gerar gráficos relacionados aos clientes
def gerar_graficos_clientes(df):
    # Gráfico de Reclamações por Faixa Etária
    fig = px.histogram(df, 
                       x='Faixa Etária', 
                       title="Distribuição de Reclamações por Faixa Etária", 
                       labels={'Faixa Etária': 'Faixa Etária'})  # Definir o rótulo correto para o eixo X
                       
    # Corrigindo o eixo Y explicitamente
    fig.update_layout(yaxis_title="Número de Reclamações")  
    st.plotly_chart(fig)

    # Gráfico de Reclamações por Sexo
    df['Sexo'] = df['Sexo'].map({'M': 'Masculino', 'F': 'Feminino', 'O': 'Outros'})
    df = df.dropna(subset=['Sexo'])
    fig = px.pie(df, names='Sexo', title="Distribuição de Reclamações por Sexo")
    st.plotly_chart(fig)

    # Gráfico de Reclamações por UF
    df_uf = df['UF'].value_counts().reset_index()
    df_uf.columns = ['UF', 'count']  # Renomeia as colunas para evitar confusão
    fig = px.bar(df_uf, 
                 x='UF', 
                 y='count', 
                 labels={'UF': 'UF', 'count': 'Número de Reclamações'}, 
                 title="Distribuição de Reclamações por Estado (UF)")
    st.plotly_chart(fig)

# Interface da página
st.title("Análise de Reclamações - Clientes")

# Upload do arquivo CSV
file = st.file_uploader("Envie o arquivo CSV", type=["csv"])

# Se o arquivo for enviado, carrega e exibe os dados
if file is not None:
    df = pd.read_csv(file, sep=';')
    
    # Exibe a tabela com paginação
    mostrar_tabela_paginada(df)
    
    # Geração dos gráficos
    gerar_graficos_clientes(df)

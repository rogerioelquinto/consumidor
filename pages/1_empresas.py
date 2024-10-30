import pandas as pd
import streamlit as st
import plotly.express as px
import math

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

# Função para gerar gráficos relacionados às empresas
def gerar_graficos_empresas(df):
    # Gráfico de empresas que mais demoraram para responder (Tempo de Resposta)
    tempo_resposta_medio = df.groupby('Nome Fantasia')['Tempo Resposta'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(tempo_resposta_medio.reset_index(), 
                 x='Nome Fantasia', 
                 y='Tempo Resposta', 
                 title="Top 10 Empresas com Maior Tempo de Resposta (média)",
                 labels={'Nome Fantasia': 'Empresas', 'Tempo Resposta': 'Tempo de Resposta (dias)'},
                 color='Tempo Resposta')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    # Gráfico de Avaliação de Reclamações
    avaliacao_reclamacao = df.groupby(['Nome Fantasia', 'Avaliação Reclamação']).size().unstack(fill_value=0).head(10)
    fig = px.bar(avaliacao_reclamacao.reset_index(), 
                 x='Nome Fantasia', 
                 y=avaliacao_reclamacao.columns, 
                 title="Distribuição de Avaliação de Reclamações",
                 labels={'Nome Fantasia': 'Empresas', 'value': 'Número de Reclamações', 'variable': 'Avaliação Reclamação'},  # Corrigindo o nome da legenda
                 barmode='stack')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    # Gráfico de Notas dos Consumidores
    fig = px.box(df.head(30), 
                 x='Nome Fantasia', 
                 y='Nota do Consumidor', 
                 title="Distribuição das Notas dos Consumidores por Empresa",
                 labels={'Nome Fantasia': 'Empresas', 'Nota do Consumidor': 'Nota do Consumidor'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Interface da página
st.title("Análise de Reclamações - Empresas")

# Upload do arquivo CSV
file = st.file_uploader("Envie o arquivo CSV", type=["csv"])

# Se o arquivo for enviado, carrega e exibe os dados
if file is not None:
    df = pd.read_csv(file, sep=';')
    
    # Exibe a tabela com paginação
    mostrar_tabela_paginada(df)
    
    # Geração dos gráficos
    gerar_graficos_empresas(df)

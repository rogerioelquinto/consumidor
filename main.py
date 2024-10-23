import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar os dados de um arquivo CSV
@st.cache_data
def carregar_dados(arquivo_csv):
    try:
        df = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para exibir a tabela com paginação
def exibir_tabela(df):
    st.subheader("Amostra de Dados")
    # Paginação na tabela
    linhas_por_pagina = st.slider('Selecione o número de linhas por página', 5, 50, 10)
    pagina_atual = st.number_input('Página', min_value=1, max_value=(len(df) // linhas_por_pagina) + 1, step=1)
    
    inicio = (pagina_atual - 1) * linhas_por_pagina
    fim = inicio + linhas_por_pagina
    st.dataframe(df.iloc[inicio:fim])

# Função para gerar gráfico das empresas com mais reclamações
def gerar_grafico_empresas(df):
    st.subheader("Empresas com Mais Reclamações")
    empresas_mais_reclamadas = df['Nome Fantasia'].value_counts().head(10)
    fig = px.bar(empresas_mais_reclamadas, x=empresas_mais_reclamadas.index, y=empresas_mais_reclamadas.values,
                 labels={'x': 'Empresas', 'y': 'Número de Reclamações'}, title="Top 10 Empresas com Mais Reclamações")
    st.plotly_chart(fig)

# Função para gerar gráfico de estados com mais reclamações
def gerar_grafico_estados(df):
    st.subheader("Estados com Mais Reclamações")
    estados_mais_reclamacoes = df['UF'].value_counts().head(10)
    fig = px.bar(estados_mais_reclamacoes, x=estados_mais_reclamacoes.index, y=estados_mais_reclamacoes.values,
                 labels={'x': 'Estados (UF)', 'y': 'Número de Reclamações'}, title="Top 10 Estados com Mais Reclamações")
    st.plotly_chart(fig)

# Função para gerar gráfico dos assuntos mais reclamados
def gerar_grafico_assuntos(df):
    st.subheader("Top 10 Assuntos Mais Reclamados")
    assuntos_mais_reclamados = df['Assunto'].value_counts().head(10)
    fig = px.bar(assuntos_mais_reclamados, x=assuntos_mais_reclamados.index, y=assuntos_mais_reclamados.values,
                 labels={'x': 'Assunto', 'y': 'Número de Reclamações'}, title="Top 10 Assuntos Mais Reclamados")
    fig.update_layout(showlegend=False)  # Remove a legenda desnecessária
    st.plotly_chart(fig)

# Função para gerar gráficos adicionais
def gerar_graficos_adicionais(df):
    st.subheader("Distribuição por Segmento de Mercado")
    fig = px.pie(df, names='Segmento de Mercado', title="Distribuição de Reclamações por Segmento de Mercado")
    st.plotly_chart(fig)

    st.subheader("Distribuição por Faixa Etária")
    faixa_etaria_count = df['Faixa Etária'].value_counts()
    fig = px.bar(faixa_etaria_count, x=faixa_etaria_count.index, y=faixa_etaria_count.values,
                 labels={'x': 'Faixa Etária', 'y': 'Número de Reclamações'}, title="Distribuição por Faixa Etária")
    st.plotly_chart(fig)

# Função principal da aplicação
def main():
    st.title("Análise de Reclamações do Consumidor")

    # Upload do arquivo CSV pelo usuário
    arquivo_csv = st.file_uploader("Selecione o arquivo CSV para análise", type="csv")

    if arquivo_csv is not None:
        df = carregar_dados(arquivo_csv)
        
        if df is not None:
            # Exibir tabela com paginação
            exibir_tabela(df)

            # Gerar gráficos
            gerar_grafico_empresas(df)
            gerar_grafico_estados(df)
            gerar_grafico_assuntos(df)
            gerar_graficos_adicionais(df)
        else:
            st.error("Erro ao carregar os dados.")

if __name__ == "__main__":
    main()

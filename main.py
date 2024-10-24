import streamlit as st
from PIL import Image

# Título do projeto
st.title("Análise de Reclamações de Consumidores")
st.markdown("""
Projeto baseado em dados públicos de reclamações de consumidores fornecidos pelo [consumidor.gov.br](https://consumidor.gov.br).
Selecione a página no menu lateral para explorar as reclamações por empresas ou clientes.
""")

# Link para o site oficial de dados públicos
st.markdown("[Clique aqui para acessar os dados públicos](https://consumidor.gov.br/pages/dadosabertos/externo/)")

# Carregar logo
logo = Image.open('consumidor_gov_br.png')
st.image(logo, use_column_width=True)

# Menu lateral
st.sidebar.title("Navegação")
st.sidebar.markdown("Escolha uma página no menu acima.")

import streamlit as st
from instalador_protheus_web import run_instalador  # Função que roda o programa Instalador Protheus
from inicializador_protheus_web import run_inicializador  # Função que roda o programa Inicializador Protheus

# Funções para cada programa
def show_home():
    # Coloca a imagem e o título juntos
    col1, col2 = st.columns([1, 10])  # Define duas colunas para a imagem e o título
    with col1:
        st.image("TOTS3.SA.ico", width=70)  # Exibe a imagem
    with col2:
        st.title("Protheus Control Center")  # Exibe o título ao lado da imagem
    
    st.write("Escolha uma das aplicações no menu lateral para começar.")
    
    st.markdown("""
    - [Documentação do Instalador Protheus](https://github.com/usuario/repositorio/docs/instalador_protheus.md)
    - [Documentação do Inicializador Protheus](https://github.com/usuario/repositorio/docs/inicializador_protheus.md)
    """)


# Menu lateral para navegação
st.sidebar.title("Protheus Control Center")
app_choice = st.sidebar.radio("Escolha a aplicação:", ["Página Inicial", "Instalador Protheus", "Inicializador Protheus"])

# Navegação com base na escolha do usuário
if app_choice == "Página Inicial":
    show_home()
elif app_choice == "Instalador Protheus":
    run_instalador()
elif app_choice == "Inicializador Protheus":
    run_inicializador()
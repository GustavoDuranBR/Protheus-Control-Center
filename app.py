import streamlit as st
from instalador_protheus_web import run_instalador  # Função que roda o programa Instalador Protheus
from inicializador_protheus_web import run_inicializador  # Função que roda o programa Inicializador Protheus
from configurador_appserver import edit_appserver_config

# Funções para cada programa
def show_home():
    # Cria uma seção de colunas para logo e título
    col1, col2 = st.columns([1, 10])

    # Alinhamento centralizado na coluna 1 (logo)
    with col1:
        st.write(" ")
        st.image("TOTS3.SA.ico", width=70)

    # Alinhamento centralizado na coluna 2 (título)
    with col2:
        st.write(" ")
        st.markdown(
            "<h1 style='text-align: justify; line-height: 0.3;'>Protheus Control Center</h1>",
            unsafe_allow_html=True
        )
    
    st.write("Escolha uma das aplicações no menu lateral para começar.")
    
    st.markdown("""
    - [Documentação do Instalador Protheus](https://github.com/GustavoDuranBR/Protheus-Control-Center/blob/master/docs/instalador_protheus.md)
    - [Documentação do Inicializador Protheus](https://github.com/GustavoDuranBR/Protheus-Control-Center/blob/master/docs/inicializador_protheus.md)
    """)


# Menu lateral para navegação
st.sidebar.title("Protheus Control Center")
app_choice = st.sidebar.radio("Escolha a aplicação:", ["Página Inicial", "Instalador Protheus", "Inicializador Protheus", "Configurar AppServer.ini"])

# Navegação com base na escolha do usuário
if app_choice == "Página Inicial":
    show_home()
elif app_choice == "Instalador Protheus":
    run_instalador()
elif app_choice == "Inicializador Protheus":
    run_inicializador()
elif app_choice == "Configurar AppServer.ini":
    edit_appserver_config()

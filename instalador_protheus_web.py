import streamlit as st
st.set_page_config(
    page_title="Instalador Protheus",
    page_icon="TOTS3.SA.ico"
    )
from funcoes_web import download_and_extract_protheus, download_base_congelada
from arquivos_adicionais_web import copiar_appserver_ini, copiar_atualiar_rpo
from opcoes_adicionais_web import open_additional_options


def run_instalador():  
    # Inicializa log_content e progress_content no session_state se não existir
    if 'log_content' not in st.session_state:
        st.session_state.log_content = []
    if 'progress_content' not in st.session_state:
        st.session_state.progress_content = ""

    # Função para atualizar o log
    def update_log(message, is_progress=False):
        if is_progress:
            st.session_state.progress_content = message
        else:
            st.session_state.log_content.append(message)
        display_logs()

    # Exibe todos os logs no painel de log
    def display_logs():
        log_content = '\n'.join(st.session_state.log_content)
        full_log_content = log_content + "\n" + st.session_state.progress_content
        log_box.markdown(
            f"""
            <div style="background-color: black; color: #00FF00; font-family: monospace; padding: 10px; 
                        border-radius: 5px; height: 350px; width: 700px; overflow-y: auto; margin-top: 20px;">
                {full_log_content}
            """,
            unsafe_allow_html=True
        )

    # Função para validar as seleções
    def validate_selections(version=None, appserver=None, build=None):
        if version and (not version or version == "Selecione a versão"):
            update_log("Por favor, selecione a versão do Protheus.")
            return False
        if appserver is not None and (not appserver or appserver == "Selecione o AppServer"):
            update_log("Por favor, selecione o AppServer.")
            return False
        if build is not None and (not build or build == "Selecione a Build"):
            update_log("Por favor, selecione a Build.")
            return False
        return True

    # Função para manipular ações dos botões
    def on_download_button_click(version, appserver, build):
        if validate_selections(version, appserver, build):
            update_log("Espere enquanto realizo o download...")
            download_and_extract_protheus(version, appserver, build, update_log)

    def on_baixar_appserver_ini_button_click(version):
        if validate_selections(version=version):
            update_log("Copiando o arquivo appserver.ini...")
            copiar_appserver_ini(version)
            update_log(f"Arquivo appserver.ini copiado para C:\\TOTVS\\Protheus_{version}\\bin\\AppServer\\appserver.ini.")

    def on_baixar_atualizador_rpo_click(version):
        if validate_selections(version=version):
            update_log(f"Copiando Atualizar_RPO_{version}.bat...")
            copiar_atualiar_rpo(version)
            update_log(f"Arquivo Atualizar_RPO copiado com sucesso para a versão {version}.")

    def on_base_congelada_button_click(version):
        if validate_selections(version=version):
            update_log("Iniciando o download da base congelada...")
            download_base_congelada(version, update_log)

    # Layout da interface
    button_display = st.empty()  # Espaço reservado para os botões
    with button_display.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("TOTS3.SA.ico", width=70)
        with col2:
            st.markdown("<div class='title-container'><h1>Instalador Protheus</h1></div>", unsafe_allow_html=True)

    # Seletor de versão
    version = st.selectbox("Selecione a versão do Protheus:", ["Selecione a versão", "12.1.2210", "12.1.2310", "12.1.2410"], key="version_selectbox")

    # Seletor de AppServer
    appserver = st.selectbox("Selecione o AppServer:", ["Selecione o AppServer", "Harpia", "Panthera Onça"], key="appserver_selectbox")

    # Seletor de Build
    build = st.selectbox("Selecione a Build:", ["Selecione a Build", "Latest", "Next", "Published"], key="build_selectbox")

    # Colunas para os botões
    col3, col4, col5, col6 = st.columns(4, gap="small")

    # Placeholder para o painel de log
    global log_box
    log_box = st.empty()

    # Botões
    with col3:
        if st.button("Realizar Download", key="btn1", use_container_width=True):
            on_download_button_click(version, appserver, build)

    with col4:
        if st.button("Baixar AppServer.ini", key="btn2", use_container_width=True):
            on_baixar_appserver_ini_button_click(version)

    with col5:
        if st.button("Atualizador RPO", key="btn3", use_container_width=True):
            on_baixar_atualizador_rpo_click(version)

    with col6:
        if st.button("Base Congelada", key="btn4", use_container_width=True):
            on_base_congelada_button_click(version)

    # Exibe os logs após os botões
    display_logs()

    # Informações do desenvolvedor
    open_additional_options(update_log)
    st.sidebar.markdown(f"**Dev**: Gustavo Duran  \n**Versão**: 1.0")

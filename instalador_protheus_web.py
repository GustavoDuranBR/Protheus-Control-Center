import streamlit as st
from log import LogDisplay  # Importa a nova classe de log
from funcoes_web import download_and_extract_protheus, download_base_congelada
from arquivos_adicionais_web import copiar_appserver_ini, copiar_atualiar_rpo
from opcoes_adicionais_web import open_additional_options

def run_instalador():  
    # Função para validar as seleções
    def validate_selections(version=None, appserver=None, build=None):
        if version and (not version or version == "Selecione a versão"):
            log_display.update_log("Por favor, selecione a versão do Protheus.", message_type="AVISO")
            return False
        if appserver is not None and (not appserver or appserver == "Selecione o AppServer"):
            log_display.update_log("Por favor, selecione o AppServer.", message_type="AVISO")
            return False
        if build is not None and (not build or build == "Selecione a Build"):
            log_display.update_log("Por favor, selecione a Build.", message_type="AVISO")
            return False
        return True

    # Funções de ação dos botões
    def on_download_button_click(version, appserver, build):
        if validate_selections(version, appserver, build):
            log_display.update_log("Espere enquanto realizo o download...", message_type="INFO")
            download_and_extract_protheus(version, appserver, build, log_display.update_log)

    def on_baixar_appserver_ini_button_click(version):
        if validate_selections(version=version):
            log_display.update_log("Copiando o arquivo appserver.ini...", message_type="INFO")
            copiar_appserver_ini(version)
            log_display.update_log(f"Arquivo appserver.ini copiado para C:\\TOTVS\\Protheus_{version}\\bin\\AppServer\\appserver.ini.", message_type="OK")

    def on_baixar_atualizador_rpo_click(version):
        if validate_selections(version=version):
            log_display.update_log(f"Copiando Atualizar_RPO_{version}.bat...", message_type="INFO")
            copiar_atualiar_rpo(version)
            log_display.update_log(f"Arquivo Atualizar_RPO copiado com sucesso para a versão {version}.", message_type="OK")

    def on_base_congelada_button_click(version):
        if validate_selections(version=version):
            log_display.update_log("Iniciando o download da base congelada...", message_type="INFO")
            download_base_congelada(version, log_display.update_log)

    # Layout da interface
    button_display = st.empty()  # Espaço reservado para os botões
    with button_display.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("TOTS3.SA.ico", width=70)
        with col2:
            st.markdown("<div class='title-container'><h1>Instalador Protheus</h1></div>", unsafe_allow_html=True)

    # Seletores de versão, AppServer e Build
    version = st.selectbox("Selecione a versão do Protheus:", ["Selecione a versão", "12.1.2210", "12.1.2310", "12.1.2410"], key="version_selectbox")
    appserver = st.selectbox("Selecione o AppServer:", ["Selecione o AppServer", "Harpia", "Panthera Onça"], key="appserver_selectbox")
    build = st.selectbox("Selecione a Build:", ["Selecione a Build", "Latest", "Next", "Published"], key="build_selectbox")

    # Colunas para os botões
    col3, col4, col5, col6 = st.columns(4, gap="small")
    
    # Inicializa a exibição de log usando a classe LogDisplay
    log_display = LogDisplay(log_height=350, log_width=700)

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

    # Exibe os logs usando a classe LogDisplay
    log_display.display_logs()

    # Informações do desenvolvedor
    open_additional_options(log_display.update_log)
    st.sidebar.markdown(f"**Dev**: Gustavo Duran  \n**Versão**: 1.0")

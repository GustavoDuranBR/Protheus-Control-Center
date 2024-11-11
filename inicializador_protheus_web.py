import streamlit as st
import subprocess
from atualizar_rpo_web import update_rpo
from config_web import paths, save_paths, load_paths
from log import LogDisplay  # Importa a classe LogDisplay do arquivo log.py

def run_inicializador():
        # Inicialize o estado de sessão para log e progresso se não existir
    if 'log_content' not in st.session_state:
        st.session_state.log_content = []  # Inicializa como uma lista vazia para armazenar logs
    if 'progress_content' not in st.session_state:
        st.session_state.progress_content = ''  # Inicializa como uma string vazia para progresso

    # Carregar configurações iniciais
    paths = load_paths()

    # Elementos de exibição de log e botões
    button_display = st.empty()

    def start_dbaccess_and_appserver():
        log_display.add_log_session("Iniciando DbAccess e AppServer")
        log_display.run_command(f'start "" "{paths["Dbaccess"]}"')
        log_display.run_command(f'start "" "{paths["Appserver"]}"')

    def start_update_rpo():
        version = paths.get("Versao_RPO", "")
        if not version:
            log_display.update_log("Erro: Versão RPO não está definida. Verifique nas Configurações.", message_type="ERRO")
            return
        log_display.add_log_session("Atualização do RPO")
        progress_updates = update_rpo(version, st.session_state.log_content, lambda msg: log_display.update_log(msg, is_progress=True)) or []
        for progress in progress_updates:
            log_display.update_log(progress, is_progress=True)
        log_display.update_log("RPO baixado com sucesso.", message_type="OK")

    def close_terminals():
        log_display.add_log_session("Fechando Terminais")
        dbaccess_close_command = "taskkill /F /IM dbaccess64.exe"
        appserver_close_command = "taskkill /F /IM appserver.exe"

        # Fechando o terminal do DbAccess
        log_display.run_command(dbaccess_close_command)
        log_display.update_log("Terminal para DbAccess fechado com sucesso.", message_type="OK")

        # Fechando o terminal do AppServer
        log_display.run_command(appserver_close_command)
        log_display.update_log("Terminal para AppServer fechado com sucesso.", message_type="OK")

        log_display.update_log("Todos os terminais foram fechados.", message_type="ERRO")

    # Sidebar para configurações
    st.sidebar.header("Configurações")
    version_options = ["Selecione a versão", "12.1.2210", "12.1.2310", "12.1.2410"]
    selected_version = st.sidebar.selectbox("Selecionar Versão RPO", version_options)
    
    st.sidebar.subheader("Configuração da Porta")
    porta = st.sidebar.number_input("Digite a porta na qual o Protheus web deve operar:", min_value=1, max_value=65535, value=8089)

    if selected_version:
        paths["Versao_RPO"] = selected_version
        paths["Appserver"] = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\Appserver\\appserver.exe - Atalho.lnk"
        paths["Smartclient"] = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\SmartClient\\smartclient.exe - Atalho.lnk"
        paths["Porta_WEBAPP"] = f"{porta}"

    st.sidebar.text_input("Caminho para DbAccess", value=paths["Dbaccess"], disabled=True)
    st.sidebar.text_input("Caminho para AppServer", value=paths["Appserver"], disabled=True)
    st.sidebar.text_input("Caminho para SmartClient", value=paths["Smartclient"], disabled=True)

    if st.sidebar.button("Salvar Configurações"):
        save_paths(paths)
        st.sidebar.success("Configurações salvas com sucesso!")

    # Informações sobre versão e desenvolvedor
    st.sidebar.markdown("**Dev**: Gustavo Duran  \n**Versão**: 1.0")

    with button_display.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("TOTS3.SA.ico", width=70)
        with col2:
            st.markdown("<div class='title-container'><h1>Inicializador Protheus</h1></div>", unsafe_allow_html=True)

        col3, col4, col5, col6 = st.columns(4, gap="small")
        
        # Cria uma instância de LogDisplay para gerenciar os logs
        log_display = LogDisplay(log_height=350, log_width=700)
        
        with col3:
            if st.button("DbAccess/AppServer", key="btn1", use_container_width=True):
                start_dbaccess_and_appserver()
        with col4:
            if st.button("Protheus WEB", key="btn2", use_container_width=True):
                web_url = f"http://localhost:{porta}"
                try:
                    subprocess.Popen(f'start {web_url}', shell=True)
                    log_display.update_log(f"Navegador aberto em {web_url}.", message_type="INFO")
                except Exception as e:
                    log_display.update_log(f"Erro ao abrir o navegador: {e}", message_type="ERRO")
        with col5:
            if st.button("Atualizar RPO", key="btn3", use_container_width=True):
                start_update_rpo()
        with col6:
            if st.button("Fechar Terminais", key="btn4", use_container_width=True):
                close_terminals()

    # Exibe o log no final
    log_display.display_logs()

import streamlit as st
import configparser
import os

# Função para carregar o arquivo de configuração
def load_config(file_path):
    config = configparser.ConfigParser()
    
    try:
        config.read(file_path)
    except configparser.DuplicateOptionError as e:
        st.error(f"Erro de duplicação no arquivo {file_path}: {e}")
        # Corrigir duplicação aqui, se necessário
        with open(file_path, 'r') as f:
            lines = f.readlines()

        corrected_lines = []
        seen_options = set()
        for line in lines:
            if '=' in line:
                option = line.split('=')[0].strip()
                if option in seen_options:
                    continue
                seen_options.add(option)
            corrected_lines.append(line)

        with open(file_path, 'w') as f:
            f.writelines(corrected_lines)

        config.read(file_path)
    
    return config

# Função para salvar as modificações no arquivo
def save_config(config, file_path):
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# Função que cria a interface para editar o arquivo appserver.ini
def edit_appserver_config():
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
            "<h1 style='text-align: justify; line-height: 0.3;'>Configurações do Appserver</h1>",
            unsafe_allow_html=True
        )

    # Sidebar para configurações
    st.sidebar.header("Configurações")
    version_options = ["Selecione a Versão", "12.1.2210", "12.1.2310", "12.1.2410"]
    selected_version = st.sidebar.selectbox("Selecionar Versão", version_options)

    # Define dbalias automaticamente com base na versão selecionada
    if selected_version == "12.1.2210":
        dbalias = "P1212210MNTDBEXP"
    elif selected_version == "12.1.2310":
        dbalias = "P1212310MNTDBEXP"
    elif selected_version == "12.1.2410":
        dbalias = "P1212410MNTDBEXP"
    else:
        dbalias = None

    # Verifica se uma versão foi selecionada
    if selected_version == "Selecione a Versão" or dbalias is None:
        st.warning("Por favor, selecione uma versão.")
        return

    # Define os caminhos com base na versão selecionada
    file_path = f"C:\\TOTVS\\Protheus_{selected_version}\\bin\\Appserver\\appserver.ini"
    dbalias_path = f"C:\\TOTVS\\Protheus_{selected_version}"

    # Verifica se o arquivo existe antes de carregar
    if os.path.exists(file_path):
        config = load_config(file_path)

        # Verifica se a seção do DbAlias selecionado existe
        if dbalias not in config:
            st.error(f"A seção {dbalias} não foi encontrada no arquivo {file_path}. Verifique se a configuração está correta.")
            return

        # Seção de configuração usando o dbalias selecionado
        db_section = dbalias

        # Campos editáveis da seção DbAlias
        st.header("DbAlias")
        dbalias = st.text_input("dbalias", value=config[db_section].get("dbalias", f"{db_section}"))
        dbserver = st.text_input("dbserver", value=config[db_section].get("dbserver", "localhost"))
        dbdatabase = st.text_input("dbdatabase", value=config[db_section].get("dbdatabase", "MSSQL"))
        dbport = st.number_input("dbport", value=int(config[db_section].get("dbport", 7890)), min_value=1, max_value=65535)
        startsysindb = st.selectbox("startsysindb", ["1", "0"], index=["1", "0"].index(config[db_section].get("startsysindb", "1")))
        theme = st.selectbox("theme", ["Light", "Dark"], index=["Light", "Dark"].index(config[db_section].get("theme", "Dark")))

        # Outros campos para edição de caminho
        sourcepath = st.text_input("sourcepath", value=config[db_section].get("sourcepath", f"{dbalias_path}\\Apo\\"))
        rootpath = st.text_input("rootpath", value=config[db_section].get("rootpath", f"{dbalias_path}\\Protheus_Data\\"))
        rpocustom = st.text_input("rpocustom", value=config[db_section].get("rpocustom", f"{dbalias_path}\\Apo\\custom.rpo"))
        startpath = st.text_input("startpath", value=config[db_section].get("startpath", "\\system\\"))

        # Seção ONSTART
        st.header("ONSTART")
        onstart_enabled = st.selectbox("Habilitar ONSTART", ["Sim", "Não"]) == "Sim"

        # Seção HTTP
        st.header("HTTP")
        http_enable = st.selectbox("HTTP Enabled", ["1", "0"], index=["1", "0"].index(config["HTTP"].get("ENABLE", "0")))
        http_port = st.number_input("Porta HTTP", value=int(config["HTTP"].get("PORT", "8080")), min_value=1, max_value=65535)
        http_path = st.text_input("Caminho HTTP", value=config["HTTP"].get("PATH", "/"))

        # Seção HTTPREST
        st.header("HTTP REST")
        rest_enable = config["HTTPREST"].get("Enable", "0")
        rest_enable = st.selectbox("HTTP REST Enabled", ["1", "0"], index=["1", "0"].index(rest_enable))
        rest_port = st.number_input("Porta HTTP REST", value=int(config["HTTPREST"].get("Port", 8080)), min_value=1, max_value=65535)

        # Seção LICENSECLIENT
        st.header("Licença")
        license_server = st.text_input("Servidor de Licença", value=config["LICENSECLIENT"].get("Server", "localhost"))
        license_port = st.number_input("Porta de Licença", value=int(config["LICENSECLIENT"].get("Port", "7889")), min_value=1, max_value=65535)

        # Seção TCP
        st.header("TCP")
        tcp_type = st.selectbox("Tipo de TCP", ["TCPIP", "SSL"], index=["TCPIP", "SSL"].index(config["TCP"].get("TYPE", "TCPIP")))
        tcp_port = st.number_input("Porta TCP", value=int(config["TCP"].get("Port", "7890")), min_value=1, max_value=65535)
        tcp_secure = st.selectbox("Conexão Segura", ["1", "0"], index=["1", "0"].index(config["TCP"].get("SecureConnection", "1")))

        # Seção WEBAPP
        st.header("WEBAPP")
        webapp_port = st.number_input("Porta WEBAPP", value=int(config["WEBAPP"].get("Port", "8089")), min_value=1, max_value=65535)

        # Atualiza as configurações com os valores fornecidos
        if st.button("Aplicar Configurações"):
            # Atualizando valores da seção HTTP
            config["HTTP"]["ENABLE"] = http_enable
            config["HTTP"]["PORT"] = str(http_port)
            config["HTTP"]["PATH"] = http_path

            # Atualizando valores da seção HTTPREST
            config["HTTPREST"]["Enable"] = rest_enable
            config["HTTPREST"]["Port"] = str(rest_port)

            # Atualizando valores da seção LICENSECLIENT
            config["LICENSECLIENT"]["Server"] = license_server
            config["LICENSECLIENT"]["Port"] = str(license_port)

            # Atualizando valores da seção TCP
            config["TCP"]["TYPE"] = tcp_type
            config["TCP"]["Port"] = str(tcp_port)
            config["TCP"]["SecureConnection"] = tcp_secure

            # Atualizando valores da seção ONSTART
            config["ONSTART"]["jobs"] = "HTTPJOB" if onstart_enabled else ""

            # Atualizando valores da seção DbAlias selecionada
            config[db_section]["dbalias"] = dbalias
            config[db_section]["dbserver"] = dbserver
            config[db_section]["dbdatabase"] = dbdatabase
            config[db_section]["dbport"] = str(dbport)
            config[db_section]["startsysindb"] = startsysindb
            config[db_section]["theme"] = theme
            config[db_section]["sourcepath"] = sourcepath
            config[db_section]["rootpath"] = rootpath
            config[db_section]["rpocustom"] = rpocustom
            config[db_section]["startpath"] = startpath

            # Atualizando porta WEBAPP
            config["WEBAPP"]["Port"] = str(webapp_port)

            # Salva o arquivo de configuração
            save_config(config, file_path)
            st.success("Configurações salvas com sucesso!")
    else:
        st.error(f"O arquivo {file_path} não foi encontrado.")

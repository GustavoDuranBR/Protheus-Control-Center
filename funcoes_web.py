import os
import zipfile
import py7zr
import requests
import streamlit as st
from win32com.client import Dispatch
import pythoncom
import subprocess

# Constantes para URLs e caminhos base
BASE_DIRECTORY = "C:\\TOTVS"
BASE_DOWNLOAD_DIRECTORY = os.path.join(BASE_DIRECTORY, "Download")
URL_BASE_APP_SERVER = "https://arte.engpro.totvs.com.br/tec/appserver/"
URL_BASE_SMART_CLIENT = "https://arte.engpro.totvs.com.br/tec/smartclient/harpia/"
URL_BASE_DB_ACCESS = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbaccess.zip"
URL_BASE_DB_API = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbapi.zip"
URL_BASE_SMART_CLIENT_WEB_APP = "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/"

def create_folder_structure(version, update_log_func):
    directories = [
        os.path.join(BASE_DIRECTORY, f"{version}", "Apo"),
        os.path.join(BASE_DIRECTORY, f"Protheus_{version}", "bin", "Appserver"),
        os.path.join(BASE_DIRECTORY, f"Protheus_{version}", "bin", "SmartClient"),
        os.path.join(BASE_DIRECTORY, f"{version}", "Protheus_data"),
        os.path.join(BASE_DIRECTORY, "TotvsDBAccess")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        update_log_func(f"Pasta criada: {directory}")
    update_log_func("Estrutura de pastas criada com sucesso.")

def get_download_url(appserver, build, version):
    # Mapeamento do tipo de appserver e build
    appserver_map = {
        "Harpia": "harpia",
        "Panthera Onça": "panthera_onca"
    }
    build_map = {
        "Latest": "latest",
        "Next": "next",
        "Published": "published"
    }
    
    urls = [
        f"{URL_BASE_APP_SERVER}{appserver_map[appserver]}/windows/64/{build_map[build]}/appserver.zip",
        f"{URL_BASE_SMART_CLIENT}/windows/64/{build_map[build]}/smartclient.zip",
        URL_BASE_DB_ACCESS,
        URL_BASE_DB_API,
        f"{URL_BASE_SMART_CLIENT_WEB_APP}{appserver_map[appserver]}/windows/64/{build_map[build]}/smartclientwebapp.zip",
        f"https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/{version}/exp_com_dic/latest/protheus_data.zip",
        f"https://arte.engpro.totvs.com.br/tec/web-agent/windows/64/latest/web-agent.zip"
    ]
    return urls

def download_file_with_progress(file_path, url, update_log_func):
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_percent = (downloaded_size / total_size) * 100 if total_size else 0
                    update_log_func(f"Progresso: {progress_percent:.2f}%", is_progress=True)
        update_log_func(f"Download concluído: {file_path}\n")
    except requests.RequestException as e:
        update_log_func(f"Erro ao baixar {url}: {str(e)}\n")
    except Exception as e:
        update_log_func(f"Erro inesperado ao baixar {url}: {str(e)}\n")

def extract_protheus_data(zip_file_path, extraction_path, update_log_func):
    """
    Extrai o arquivo protheus_data.zip para o diretório especificado usando py7zr.
    
    Parâmetros:
    - zip_file_path: Caminho completo do arquivo ZIP do Protheus.
    - extraction_path: Caminho do diretório onde os arquivos serão extraídos.
    - log_func: Função de callback para mensagens de log (opcional).
    """
    if update_log_func is None:
        update_log_func = print  # Define como padrão a função print se nenhuma função de log for passada

    if not os.path.exists(zip_file_path):
        update_log_func(f"Erro: O arquivo {zip_file_path} não foi encontrado.")
        return

    if not os.path.exists(extraction_path):
        os.makedirs(extraction_path, exist_ok=True)
        update_log_func(f"Pasta de extração criada: {extraction_path}")
    
    try:
        update_log_func(f"Iniciando extração do arquivo {zip_file_path} para {extraction_path}...")
        with py7zr.SevenZipFile(zip_file_path, 'r') as archive:
            archive.extractall(path=extraction_path)
        update_log_func(f"Extração de {zip_file_path} concluída com sucesso em {extraction_path}.")
    except Exception as e:
        update_log_func(f"Erro ao extrair {zip_file_path}: {str(e)}")

def extract_files(file_path, extraction_path, update_log_func):
    os.makedirs(extraction_path, exist_ok=True)
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            try:
                update_log_func(f"Extraindo {os.path.basename(file_path)} para {extraction_path}...")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extraction_path)
                update_log_func(f"Extração de {os.path.basename(file_path)} concluída.\n")
            except zipfile.BadZipFile:
                update_log_func(f"Erro: {os.path.basename(file_path)} não é um arquivo ZIP válido.\n")
            except Exception as e:
                update_log_func(f"Erro ao extrair {os.path.basename(file_path)}: {str(e)}\n")
        else:
            update_log_func(f"Erro: {os.path.basename(file_path)} está vazio ou corrompido.\n")
    else:
        update_log_func(f"Arquivo {os.path.basename(file_path)} não encontrado para extração.\n")

def download_and_extract_protheus(version, appserver, build, update_log_func):
    create_folder_structure(version, update_log_func)
    urls = get_download_url(appserver, build, version)
    download_path = os.path.join(BASE_DOWNLOAD_DIRECTORY, version)
    os.makedirs(download_path, exist_ok=True)

    extraction_map = {
        "appserver.zip": os.path.join(BASE_DIRECTORY, f"Protheus_{version}", "bin", "Appserver"),
        "smartclient.zip": os.path.join(BASE_DIRECTORY, f"Protheus_{version}", "bin", "SmartClient"),
        "dbaccess.zip": os.path.join(BASE_DIRECTORY, "TotvsDBAccess"),
        "dbapi.zip": os.path.join(BASE_DIRECTORY, "TotvsDBAccess"),
        "smartclientwebapp.zip": os.path.join(BASE_DIRECTORY, f"Protheus_{version}", "bin", "Appserver"),
        "protheus_data.zip": os.path.join(BASE_DIRECTORY, f"{version}")
    }

    for url in urls:
        file_name = url.split("/")[-1]
        file_path = os.path.join(download_path, file_name)
        update_log_func(f"Iniciando download de {file_name}...")
        download_file_with_progress(file_path, url, update_log_func)
        
        if file_name in extraction_map:
            extraction_path = extraction_map[file_name]
            
            # Chamar a função extract_protheus_data para extrair o arquivo de dados do Protheus
            if file_name == "protheus_data.zip":
                extract_protheus_data(file_path, extraction_path, update_log_func)  # Chamando a função correta
            else:
                # Se for outro arquivo, utilizar a função genérica ou o método de extração desejado
                extract_files(file_path, extraction_path, update_log_func)

    create_appserver_shortcut(update_log_func, version)
    create_smartclient_shortcut(update_log_func, version)
    create_dbaccess_shortcut(update_log_func)
    update_log_func("Todos os arquivos foram baixados, extraídos, e os atalhos foram criados com sucesso.\n")

def create_shortcut(file_path, shortcut_name, additional_parameters, update_log_func):
    try:
        pythoncom.CoInitialize()
        if not os.path.exists(file_path):
            update_log_func(f"Erro: Arquivo {file_path} não encontrado.\n")
            return
        shortcut_path = os.path.join(os.path.dirname(file_path), f"{shortcut_name}.lnk")
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = file_path
        shortcut.Arguments = additional_parameters
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.save()
        update_log_func(f"Atalho criado: {shortcut_path}")
    except Exception as e:
        update_log_func(f"Erro ao criar atalho para {shortcut_name}: {str(e)}\n")

# Funções específicas para criar atalhos de cada componente
def create_appserver_shortcut(update_log_func, version):
    appserver_path = f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver\\appserver.exe"
    create_shortcut(appserver_path, "appserver.exe - Atalho", "-console", update_log_func)

def create_smartclient_shortcut(update_log_func, version):
    smartclient_path = f"C:\\TOTVS\\Protheus_{version}\\bin\\SmartClient\\smartclient.exe"
    create_shortcut(smartclient_path, "smartclient.exe - Atalho", " -m", update_log_func)

def create_dbaccess_shortcut(update_log_func):
    dbaccess_path = r"C:\\TOTVS\\TotvsDBAccess\\dbaccess64.exe"
    create_shortcut(dbaccess_path, "dbaccess64.exe - Atalho", "-debug", update_log_func)

# Função para download da base congelada
def download_base_congelada(version, update_log_func):
    version_map = {
        "12.1.2210": "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2210/exp_com_dic/latest/mssql_bak.zip",
        "12.1.2310": "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2310/exp_com_dic/latest/mssql_bak.zip",
        "12.1.2410": "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2410/exp_com_dic/latest/mssql_bak.zip"
    }
    if version not in version_map:
        update_log_func("Versão inválida para download da base congelada.\n")
        return

    url = version_map[version]
    # Caminho para salvar o arquivo
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    os.makedirs(base_directory, exist_ok=True)
    file_path = os.path.join(base_directory, "mssql_bak.zip")
    update_log_func(f"Iniciando download da base congelada: {url}")
    download_file_with_progress(file_path, url, update_log_func)

def install_web_agent(update_log_func, version):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    web_agent_path = os.path.join(base_directory, "web-agent")

    try:
        # Verifica se o diretório existe
        if not os.path.exists(web_agent_path):
            update_log_func(f"Caminho não encontrado: {web_agent_path}\n")
            return
        
        # Lista todos os arquivos no diretório web-agent e filtra arquivos .exe
        files = os.listdir(web_agent_path)
        exe_files = [file for file in files if file.endswith('.exe')]

        if exe_files:
            setup_file = os.path.join(web_agent_path, exe_files[0])
            update_log_func(f"Arquivo de instalação encontrado: {setup_file}")

            # Executa o comando de instalação de forma silenciosa
            update_log_func(f"Iniciando a instalação do {setup_file}...")
            subprocess.run([setup_file, "/silent"], check=True)

            update_log_func(f"Instalação do {setup_file} concluída com sucesso!\n")
        else:
            update_log_func("Nenhum arquivo de instalação (.exe) encontrado no diretório web-agent.\n")
    except Exception as e:
        update_log_func(f"Erro durante a instalação: {str(e)}\n")

# Definir uma variável global para armazenar as mensagens de log
log_container = st.empty()
log_messages = ""

def update_log(message, is_progress=False):
    global log_messages
    if not is_progress:
        # Adicionar a nova mensagem ao log
        log_messages += f"{message}\n"
        # Renderizar o log completo na área vazia, que será atualizada automaticamente
        log_container.text(log_messages)

    else:
        # Caso seja progresso, exibir uma barra de progresso (opcional)
        st.progress(float(message.strip('%')) / 100)

# Função principal para inicializar o download com a atualização de log
def initialize_download(version, appserver, build):
    download_and_extract_protheus(version, appserver, build, update_log)
    download_base_congelada(version, update_log)

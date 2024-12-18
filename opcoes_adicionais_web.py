import streamlit as st
from bs4 import BeautifulSoup
import requests
import os
import time
from log import LogDisplay

# URLs base para download e obtenção de versões
base_urls = {
    "AppServer": "https://arte.engpro.totvs.com.br/tec/appserver/{}/windows/64/builds/",
    "SmartClientWebApp": "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/{}/windows/64/builds/",
    "Web-Agent": "https://arte.engpro.totvs.com.br/tec/web-agent/windows/64/builds/"
}

build_mapping = {
    "Panthera Onça": "panthera_onca",
    "Harpia": "harpia"
}

log_display = LogDisplay()  # Inicializa o log para o sistema

def get_versions(url):
    try:
        # Ignora a verificação SSL para contornar o erro do certificado expirado
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('tr.file')
        versions = []
        for row in rows:
            version_tag = row.select_one('td:nth-child(2) span.name')
            if version_tag:
                version_name = version_tag.get_text(strip=True)
                versions.append(version_name)
        return versions
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter versões de {url}: {str(e)}")
        return []

def verificar_e_criar_diretorio():
    base_directory = "C:\\TOTVS\\Download\\Download_Protheus"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
        return f"Diretório {base_directory} criado com sucesso."
    return f"Diretório {base_directory} já existe."

def realizar_download(url, destino, log_func):
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(destino, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Atualiza o progresso na mesma linha
                    percent_complete = (downloaded_size / total_size) * 100
                    progress_message = f"Baixando {os.path.basename(destino)}: {percent_complete:.2f}% concluído\n"
                    log_func(progress_message, is_progress=True)
        
        # Conclui o download e adiciona ao log
        log_func(f"Download de {os.path.basename(destino)} concluído.\n")
    except Exception as e:
        log_func(f"Erro ao baixar {os.path.basename(destino)}: {str(e)}\n")

def iniciar_download(options, log_func, build_var):
    total_steps = sum(1 for selected in options.keys()) * 2 + 2
    current_step = 0

    def update_log(message, is_progress=False):
        nonlocal current_step
        if not is_progress:
            current_step += 1
        log_func(f"[{current_step}/{total_steps}] {message}", is_progress=is_progress)

    update_log("\n==== Verificando diretório de download ====\n")
    update_log(verificar_e_criar_diretorio())
    update_log("\n==== Iniciando downloads ====\n")

    build = build_mapping.get(build_var.lower(), build_var).lower()
    for label, info in options.items():
        version = info['version']
        if label == "AppServer":
            file_name = "appserver.zip"
        elif label == "SmartClientWebApp":
            file_name = "smartclientwebapp.zip"
        elif label == "Web-Agent":
            file_name = "web-agent.zip"
        else:
            continue

        url = f"{info['url'].rstrip('/')}/{version.rstrip('/')}/{file_name}"
        build_dir = f"C:\\TOTVS\\Download\\Download_Protheus\\{build}"
        
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        destino = os.path.join(build_dir, file_name)
        update_log(f"Preparando download de {label} - Versão {version}...\n")
        realizar_download(url, destino, update_log)

    update_log("\n==== Todos os downloads foram concluídos ====\n")

def open_additional_options(update_log):
    st.sidebar.title("Opções Adicionais de Download")

    selected_build = st.sidebar.selectbox("Selecione a Build:", list(build_mapping.keys()))
    build = build_mapping[selected_build]

    options = {}
    for label in base_urls.keys():
        if st.sidebar.checkbox(f"Baixar {label}"):
            url = base_urls[label].format(build)
            versions = get_versions(url)
            if versions:
                options[label] = {
                    "version": st.sidebar.selectbox(f"Escolha a versão para {label}", versions),
                    "url": url
                }
            else:
                st.sidebar.write(f"Não há versões disponíveis para {label}.")

    if st.sidebar.button("Iniciar Download"):
        iniciar_download(options, update_log, build_var=selected_build)

def update_log_display():
    log_box = st.empty()
    while True:
        log_display(log_box)
        time.sleep(1)

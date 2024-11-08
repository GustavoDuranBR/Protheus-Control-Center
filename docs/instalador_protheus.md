# Documentação do Instalador Protheus

O **Instalador Protheus** é uma aplicação que automatiza a instalação e configuração do sistema Protheus, facilitando o processo de download de arquivos essenciais, configuração do `appserver.ini`, criação de diretórios necessários e atualização de componentes. 
Este guia detalha como utilizar o instalador, descrevendo suas funcionalidades e orientações para personalização.

## Índice
1. [Funcionalidades Principais](#funcionalidades-principais)
   - [Realizar Download](#1-realizar-download)
   - [Baixar AppServer.ini](#2-baixar-appserverini)
   - [Baixar Base Congelada](#3-baixar-base-congelada)
   - [Criação Automática de Diretórios](#4-criação-automática-de-diretórios)
   - [Atualização do RPO](#5-atualização-do-rpo)
2. [Fluxo de Execução](#fluxo-de-execução)
3. [Configuração do Arquivo appserver.ini](#configuração-do-arquivo-appserverini)
4. [Instruções de Instalação](#instruções-de-instalação)
5. [Personalização e Customização](#personalização-e-customização)
6. [Troubleshooting](#troubleshooting)
7. [Licenciamento e Contato](#licenciamento-e-contato)

---

## Funcionalidades Principais

### 1. Realizar Download
   - **Descrição**: Automatiza o download dos arquivos necessários para a instalação do Protheus, incluindo AppServer, SmartClient, DBAccess e SmartClientWebApp, conforme a versão, AppServer e build escolhidos.
   - **Uso**: Escolha a versão, AppServer e build desejados, clique em "Realizar Download".
   - **Código Relevante**:
     - `get_download_url`: Constrói as URLs de download baseadas na seleção do usuário.
     - `download_files`: Realiza o download dos arquivos.

### 2. Baixar AppServer.ini
   - **Descrição**: Baixa e configura o arquivo `appserver.ini` com os parâmetros específicos da versão selecionada.
   - **Uso**: Selecione a versão desejada e clique em "Baixar AppServer.ini" para copiar o arquivo ao diretório correto.
   - **Código Relevante**:
     - `copiar_appserver_ini`: Executa a cópia do arquivo `appserver.ini` para o diretório de destino.

### 3. Baixar Base Congelada
   - **Descrição**: Baixa a base de dados congelada específica para a versão do Protheus escolhida.
   - **Uso**: Clique em "Base Congelada" após selecionar a versão desejada.
   - **Código Relevante**:
     - `download_base_congelada`: Baixa o arquivo da base congelada.

### 4. Criação Automática de Diretórios
   - **Descrição**: Cria automaticamente a estrutura de diretórios necessária para a instalação.
   - **Uso**: Os diretórios são criados automaticamente quando o download é iniciado.
   - **Código Relevante**:
     - `create_folder_structure`: Cria a estrutura de diretórios padrão.

### 5. Atualização do RPO
   - **Descrição**: Copia o script de atualização do RPO para o diretório de destino, permitindo a atualização fácil do ambiente.
   - **Uso**: Clique em "Baixar Atualizador RPO" para copiar o script.
   - **Código Relevante**:
     - `copiar_atualiar_rpo`: Realiza a cópia do script de atualização do RPO.

---

## Fluxo de Execução

### Passo a Passo
1. **Escolha a Versão**: Selecione a versão desejada do Protheus para baixar e configurar.
2. **Configuração do AppServer**: Selecione o tipo de AppServer (Harpia, Lobo Guara, Panthera Onça) e a build (Latest, Next, Published).
3. **Download dos Arquivos**: Clique em "Realizar Download" para iniciar o processo de download dos arquivos e criação da estrutura de diretórios.
4. **Configuração do `appserver.ini`**: Clique em "Baixar AppServer.ini" para configurar o arquivo de acordo com a versão selecionada.
5. **Atualização do RPO**: Clique em "Baixar Atualizador RPO" para baixar o script de atualização.
6. **Base Congelada**: Clique em "Base Congelada" para baixar a base de dados correspondente.
7. **Opções Adicionais**: Acesse configurações extras e opções de download adicionais clicando em "Opções Adicionais".
8. **Finalizar**: Para sair, clique em "Sair" e finalize o programa.

---

## Configuração do Arquivo `appserver.ini`

Após a instalação, o arquivo `appserver.ini` pode ser editado para personalizar as configurações conforme o ambiente:

- **Parâmetro de Conexão ao Servidor**:
  ```ini
  DBServer=localhost
  ```
  Altere `localhost` para o endereço do servidor conforme necessário.

### Como Obter o Nome do Host
Para configurar o parâmetro `DBServer`, é importante conhecer o nome do host da sua máquina:

- **Windows**:
   - Abra o Prompt de Comando e digite `hostname`, pressionando Enter.
- **Linux/MacOS**:
   - No Terminal, digite `hostname` e pressione Enter.

---

## Instruções de Instalação

### Pré-requisitos
Certifique-se de ter o Python instalado e configure um ambiente virtual.

### Instalação do Programa

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seuusuario/Instalador_Protheus.git
   cd Instalador_Protheus
   ```

2. **Criação e Ativação do Ambiente Virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Instalação das Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execução da Aplicação**:
   ```bash
   python instalador_protheus.py
   ```

---

## Personalização e Customização

O **Instalador Protheus** foi projetado para fácil personalização. Aqui estão algumas sugestões de customizações adicionais:

- **Configuração do `appserver.ini`**: Personalize parâmetros como `DBServer`, `User` e `Password` conforme as credenciais e o ambiente.
- **Scripts de Atualização**: Modifique ou adicione novos scripts na pasta `scripts` caso precise de scripts de atualização diferentes para o RPO.
- **Estrutura de Diretórios**: O programa permite modificar a estrutura de diretórios padrão definida em `create_folder_structure`. Adapte esta função caso precise de uma hierarquia de pastas personalizada.

---

## Troubleshooting

Caso enfrente algum problema, consulte as seguintes orientações:

- **Problema de Download**: Certifique-se de que as URLs estão corretas e ativas. Verifique a função `get_download_url`.
- **Erro na Configuração do `appserver.ini`**: Verifique se o arquivo está sendo copiado para o diretório correto e se os parâmetros estão configurados adequadamente.
- **Erro no Ambiente Virtual**: Caso tenha dificuldades em ativar o ambiente virtual, confira as configurações do `venv` e a instalação do Python.

**Obs**: Para que as funções de download funcionem corretamente, precisa estar conectado na VPN para ter acesso aos repositórios.

---

## Licenciamento e Contato

- **Licença**: Este projeto está sob a Licença MIT. Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).
- **Autor**: Desenvolvido por Gustavo Duran.
- **Suporte e Contato**: Para dúvidas ou ajuda, entre em contato via email: gustavoduran22@gmail.com

---
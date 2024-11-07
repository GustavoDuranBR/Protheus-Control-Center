# Protheus Control Center
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

Este programa facilita a instalação e configuração do Protheus, automatizando o download de arquivos essenciais, configuração do `appserver.ini`, e a criação de diretórios necessários.


O **Protheus Control Center** é uma aplicação web simplificada para instalação e inicialização dos componentes do sistema Protheus, agilizando a configuração de ambiente e download de arquivos essenciais. Com um painel de controle intuitivo, ele permite configurar o `appserver.ini`, criar diretórios necessários, gerenciar scripts e facilita o uso de arquivos como RPOs e bases congeladas.

## Funcionalidades

- **Painel de Controle Completo**:
  - Interface intuitiva para instalar e iniciar componentes, configurável de acordo com as necessidades do usuário.
  
- **Download Automático**: 
  - Baixa arquivos essenciais (AppServer, SmartClient, DBAccess e SmartClientWebApp) com base na versão, AppServer e Build escolhidos.
  - **Código Relevante**: `get_download_url` para construir URLs, `download_files` para realizar o download.

- **Configuração do AppServer**:
  - Facilita o download e ajuste do `appserver.ini` para a versão desejada, além de disponibilizar o arquivo na estrutura correta.
  - **Código Relevante**: `copiar_appserver_ini`.

- **Base Congelada**:
  - Baixa e configura automaticamente a base de dados necessária para a versão selecionada.
  - **Código Relevante**: `download_base_congelada`.

- **Estrutura de Diretórios Automatizada**:
  - Cria a estrutura de diretórios exigida pelo sistema Protheus.
  - **Código Relevante**: `create_folder_structure`.

- **Atualização do RPO**:
  - Gera scripts automatizados para atualizar o RPO de acordo com a versão, evitando erros manuais.
  - **Código Relevante**: `copiar_atualizar_rpo`.

- **Opções Adicionais de Configuração**:
  - Interface para ajustar parâmetros adicionais de instalação e escolher opções avançadas.

### Documentação Detalhada

Para configurações avançadas e mais informações, consulte a [documentação de configurações](docs/CONFIGURACOES_DIRETORIOS.md).

---

## Estrutura do Projeto

```plaintext
ProtheusControlCenter/
│
├── funcoes.py                   # Funções principais do programa
├── gerar_appserver_ini.py       # Função para gerenciar o appserver.ini
├── protheuscontrolcenter.py     # Arquivo principal da aplicação web
├── icon.ico                     # Ícone do aplicativo
├── README.md                    # Documentação do projeto
└── venv/                        # Ambiente virtual (excluído do versionamento)
```

## Instruções de Instalação

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/seuusuario/ProtheusControlCenter.git
   cd ProtheusControlCenter
   ```

2. **Configuração do Ambiente com Poetry**:
   Instale [Poetry](https://python-poetry.org/) para gerenciar o ambiente virtual e as dependências do projeto.
   ```bash
   poetry install
   ```

3. **Execute o programa**:
   ```bash
   poetry run streamlit run protheuscontrolcenter.py
   ```

## Uso

1. Acesse o **Painel de Controle Web** da aplicação.
2. **Selecione Versão e Build**: Configure a versão, AppServer, e Build do Protheus.
3. **Opções de Configuração**:
   - Realizar Download
   - Baixar `appserver.ini`
   - Base Congelada
   - Atualização do RPO
   - Opções Adicionais
4. **Iniciar e Parar Componentes**: Utilize o painel para controlar o início e parada dos serviços do Protheus.

## Configuração do `appserver.ini`

1. Edite `appserver.ini` de acordo com as configurações locais, como `DBServer`, `Port`, entre outros parâmetros.
2. Exemplo de ajuste:
   ```plaintext
   DBServer=localhost
   ```

## Autor

Desenvolvido por Gustavo Duran.

## Licença

Este projeto está sob a Licença MIT. Consulte [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou suporte:
Email: gustavoduran22@icloud.com  
YouTube: [DuranGames](https://www.youtube.com/@DuranGames)

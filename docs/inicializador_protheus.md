# Índice da Documentação do Inicializador Protheus

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Requisitos de Instalação](#requisitos-de-instalação)
5. [Instalação](#instalação)
    - [Clonando o Repositório](#clonando-o-repositório)
    - [Criando e Ativando um Ambiente Virtual](#criando-e-ativando-um-ambiente-virtual)
    - [Instalando Dependências](#instalando-dependências)
6. [Uso](#uso)
    - [Executando a Aplicação Web](#executando-a-aplicação-web)
    - [Configuração dos Caminhos](#configuração-dos-caminhos)
    - [Atualização do RPO](#atualização-do-rpo)
7. [Documentação de Configurações](#documentação-de-configurações)
8. [Estrutura do Projeto](#estrutura-do-projeto)
9. [Contribuição](#contribuição)
10. [Licença](#licença)
11. [Contato](#contato)

---

## Sobre o Projeto

A aplicação **Inicializador Protheus** facilita a execução de tarefas críticas do sistema Protheus, como a gestão dos serviços `DbAccess` e `AppServer`, através de uma interface gráfica web desenvolvida com **Streamlit**. Esta ferramenta permite iniciar, monitorar e encerrar os serviços relacionados ao Protheus, além de oferecer logs em tempo real para acompanhar os processos em execução.

---

## Funcionalidades

1. **Iniciar e Reiniciar Serviços**  
   Permite o início ou reinício do `DbAccess` e `AppServer` através de um único botão.

2. **Monitoramento em Tempo Real**  
   Exibe logs atualizados em tempo real para acompanhamento das operações.

3. **Configuração e Persistência de Caminhos**  
   Os caminhos dos executáveis do Protheus podem ser configurados e salvos, garantindo que estejam sempre acessíveis para novas execuções.

4. **Atualização do RPO**  
   O download e atualização do RPO podem ser realizados diretamente pela interface.

5. **Exibição Personalizada de Logs**  
   A interface dos logs possui um estilo de PowerShell com cores similares ao Git Bash, proporcionando uma experiência visual aprimorada.

6. **Encerramento Automático de Serviços**  
   Ao sair da aplicação ou clicar em "Fechar Terminais", todos os serviços iniciados são automaticamente encerrados.

---

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework para backend da aplicação.
- **Streamlit**: Interface gráfica para exibição web.
- **Requests**: Gerenciamento de requisições HTTP.
- **JSON**: Utilizado para armazenamento e carregamento das configurações de diretórios.
- **Tkinter**: Originalmente usado para a interface gráfica, substituído pela interface web em Streamlit.
- **PowerShell (Visual)**: Estilo visual para os logs exibidos na interface Streamlit.

---

## Requisitos de Instalação

- **Python 3.6** ou superior
- Bibliotecas: Flask, Streamlit, Requests, JSON
- (Opcional) Tkinter para testes em modo desktop

---

## Instalação

### Clonando o Repositório

Faça o clone do repositório e entre na pasta do projeto:

```sh
git clone https://github.com/seuusuario/projeto_inicializador_protheus.git
cd projeto_inicializador_protheus
```

### Criando e Ativando um Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```sh
python -m venv venv

# No Windows
venv\Scripts\activate

# No macOS/Linux
source venv/bin/activate
```

### Instalando Dependências

Instale todas as dependências listadas no arquivo `requirements.txt`:

```sh
pip install -r requirements.txt
```

---

## Uso

### Executando a Aplicação Web

Para iniciar a aplicação, execute o comando abaixo, que abrirá o sistema no navegador:

```sh
streamlit run inicializador_protheus.py
```

### Configuração dos Caminhos

Acesse a aba de configurações na interface web para configurar os caminhos dos executáveis, tais como `DbAccess`, `AppServer` e `SmartClient`. Esse processo inclui:

1. Selecionar os executáveis desejados para cada caminho.
2. Salvar as configurações para que o sistema possa utilizá-las em futuras execuções.

### Atualização do RPO

A funcionalidade de atualização permite baixar e atualizar o RPO diretamente pela interface:

1. Selecione a versão desejada do RPO.
2. Inicie o download e acompanhe o progresso na área de logs.

---

## Documentação de Configurações

Para configurar corretamente os diretórios do sistema Protheus, consulte a [documentação de configurações](docs/CONFIGURACOES_DIRETORIOS.md). Esta documentação contém detalhes sobre a organização de diretórios, opções de configuração e especificações de cada arquivo necessário para o funcionamento.

---
### Como Contribuir

Sinta-se à vontade para contribuir com o projeto. O processo de contribuição envolve:

1. **Fork do Repositório**: Faça um fork do projeto para sua conta.
2. **Criação de uma Branch**: Crie uma branch para sua funcionalidade ou correção com o comando `git checkout -b minha-feature`.
3. **Commit das Alterações**: Salve suas alterações com `git commit -am 'Descrição das alterações'`.
4. **Push para a Branch**: Envie suas alterações para a branch com `git push origin minha-feature`.
5. **Pull Request**: Abra um Pull Request no repositório original para análise e aprovação.

---

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para obter detalhes sobre o uso e as permissões.

---

## Contato

Para dúvidas, sugestões ou contribuições, entre em contato com **Gustavo Duran** através do email: [gustavoduran22@gmail.com](mailto:gustavoduran22@gmail.com). 

---
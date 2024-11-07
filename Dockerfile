# Usando uma imagem base de Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instalar as dependências do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Condicionalmente instalar pywin32 se o sistema for Windows
RUN if [ "$(uname)" != "Darwin" ] && [ "$(uname)" != "Linux" ]; then pip install pywin32==308; fi

# Copiar o restante dos arquivos do projeto
COPY . .

# Expor a porta que sua aplicação vai rodar
EXPOSE 8501

# Definir o comando para iniciar a aplicação
CMD ["python", "app.py"]

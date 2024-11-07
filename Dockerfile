# Baixa a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia todos os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Executa o Streamlit quando o contêiner iniciar
CMD ["streamlit", "run", "inicializador_protheus_web.py"]

# Use a imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação para o container
COPY . .

# Define a variável de ambiente para não gerar bytecode (.pyc)
ENV PYTHONDONTWRITEBYTECODE=1
# Define a variável de ambiente para que o Python não faça buffering na saída
ENV PYTHONUNBUFFERED=1

# Expõe a porta 8000 para acesso à aplicação
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

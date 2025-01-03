FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação (incluindo a pasta lib_kafka)
COPY . .

# Expõe a porta que o FastAPI está utilizando
EXPOSE 8000

# Comando para rodar o app FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

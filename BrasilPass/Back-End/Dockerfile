# Usar uma imagem com Python 3.12.x
# Usar uma imagem com Python 3.12.x
FROM python:3.12-slim

# Instalar dependências do sistema para PostgreSQL e o compilador gcc
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH" 

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Configurar o Poetry
RUN poetry config installer.max-workers 10

# Instalar dependências
RUN poetry install --no-interaction --no-ansi

# Expor a porta da aplicação
EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 app.main:app
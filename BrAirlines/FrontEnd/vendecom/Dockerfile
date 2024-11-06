# Use uma imagem base com Node.js
FROM node:18-alpine

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências
COPY package.json package-lock.json ./

# Instale as dependências
RUN npm install

# Copie o restante dos arquivos da aplicação
COPY . .

# Construa o projeto para produção
RUN npm run build

# Exponha a porta que o Vite usa (padrão é 5173)
EXPOSE 5173

# Comando para iniciar o servidor de desenvolvimento Vite
CMD ["npm", "run", "dev"]
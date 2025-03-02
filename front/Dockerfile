# Imagen base
FROM node:18-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Exponer el puerto que usa Angular (por defecto 4200)
EXPOSE 4200

# Comando para iniciar la aplicación
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--disable-host-check"]

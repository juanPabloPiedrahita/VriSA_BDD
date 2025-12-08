#Hay un problema con el contenedor de Expo, no pude hacer containerizar la app movil correctamente, pero este Dockerfile sirve como referencia para futuras implementaciones,por ahora la app movil se corre localmente sin Docker.

FROM node:20 

WORKDIR /app

RUN npm install -g expo-cli

COPY package.json package-lock.json ./
RUN npm install

COPY . .

CMD ["expo", "start", "--tunnel"]

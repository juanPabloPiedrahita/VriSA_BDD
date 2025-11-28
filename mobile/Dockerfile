FROM node:20

WORKDIR /app

RUN npm install -g expo-cli

COPY package.json package-lock.json ./
RUN npm install

COPY . .

CMD ["expo", "start", "--tunnel"]

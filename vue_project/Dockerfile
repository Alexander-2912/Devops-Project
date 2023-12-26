FROM node:18

WORKDIR /frontend

COPY package*.json ./
COPY .env ./

RUN npm install
COPY . .

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "preview"]
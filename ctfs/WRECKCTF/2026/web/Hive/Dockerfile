FROM node:20-slim
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY server.js .
COPY views/ views/
RUN mkdir -p public
COPY flag.txt /flag.txt
EXPOSE 8080
CMD ["node", "server.js"]

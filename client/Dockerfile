FROM node:alpine3.16

WORKDIR /pr_client

COPY package.json .

RUN npm install

COPY ./public ./public
COPY ./src ./src

ENTRYPOINT [ "npm", "run", "start" ]
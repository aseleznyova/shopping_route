FROM node:alpine3.16 AS build

WORKDIR /pr_client

COPY package.json .

RUN npm install

COPY ./public ./public
COPY ./src ./src

RUN npm run build

FROM nginx:1.17.1-alpine
COPY ./nginx.conf.template /nginx.conf.template
COPY --from=build /pr_client/build /usr/share/nginx/html
CMD ["/bin/sh" , "-c" , "envsubst < /nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"]
FROM node:18.12.1-alpine as builder

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY package.json /usr/src/app/

RUN npm install

COPY . .

RUN npm run build

FROM nginx:1.21.3-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/app/dist/browser-interface /us/share/nginx/html

CMD ["/bin/sh",  "-c",  "envsubst < /us/share/nginx/html/assets/env.template.js > /us/share/nginx/html/assets/env.js && exec nginx -g 'daemon off;'"]
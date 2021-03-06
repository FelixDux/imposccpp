FROM node:alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
    
FROM nginx
COPY --from=0 /app/build /usr/share/nginx/html

CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf" && nginx -g 'daemon off;'
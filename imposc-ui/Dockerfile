FROM node:alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
    
FROM nginx
COPY default.conf.template /etc/nginx/templates/
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=0 /app/build /usr/share/nginx/html

RUN envsubst
FROM node:alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .

ARG REACT_APP_IMPOSC_URL
ARG REACT_APP_IMPOSC_PORT

ENV REACT_APP_IMPOSC_URL $REACT_APP_IMPOSC_URL
ENV REACT_APP_IMPOSC_PORT $REACT_APP_IMPOSC_PORT

RUN npm run build
    
FROM nginx

COPY --from=0 /app/build /usr/share/nginx/html

EXPOSE 80

RUN envsubst
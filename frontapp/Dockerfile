
FROM node:18-alpine as build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM httpd:2.4
COPY --from=build /app/build/ /usr/local/apache2/htdocs/

EXPOSE 80
CMD ["httpd-foreground"]
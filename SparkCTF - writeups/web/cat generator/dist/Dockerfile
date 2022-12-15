# docker build -t cat-generator .
# docker run --rm -it -p 8000:80 -d cat-generator

FROM php:8.1.2-apache

COPY ./challenge /var/www/html

COPY ./flag.txt /

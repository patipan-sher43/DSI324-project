FROM mysql/mysql-server:5.5.62
ENV MYSQL_ROOT_PASSWORD=ccstu_2022

COPY ./Data.sql /home/Data.sql
COPY ./db_custom_init.sh /docker-entrypoint-initdb.d/

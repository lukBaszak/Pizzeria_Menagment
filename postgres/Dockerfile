FROM postgres:11.1-alpine
#RUN ["mkdir", "/docker-entrypoint-initdb.d"]
COPY /pg_init/init.sh /docker-entrypoint-initdb.d/

FROM postgres:13.2

COPY ./compose/postgres/maintenance /usr/local/bin/maintenance
LABEL name="vanir-postgres"
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

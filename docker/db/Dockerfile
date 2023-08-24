FROM postgres:15.4

COPY z-init-user-db.sh /docker-entrypoint-initdb.d/
COPY postgres.conf /etc/postgresql/postgresql.conf
COPY postgres.conf /etc/postgresql/postgresql.test.conf

RUN chmod 0755 /docker-entrypoint-initdb.d/z-init-user-db.sh

RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/pg_hba.conf


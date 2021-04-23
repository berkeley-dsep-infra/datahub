FROM postgres:13.1

# Install python3 language extension from https://wiki.postgresql.org/wiki/Apt
RUN apt-get update && \
    apt-get install --yes \
        postgresql-plpython3-${PG_MAJOR} && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

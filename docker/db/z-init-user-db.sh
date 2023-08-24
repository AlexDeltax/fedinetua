#!/bin/bash
set -ex

psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE USER fedi_user WITH PASSWORD 's3cr3t';
    ALTER ROLE fedi_user SET client_encoding TO 'utf8';
    ALTER ROLE fedi_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE fedi_user SET timezone TO 'UTC';
    ALTER USER fedi_user CREATEDB;
    CREATE DATABASE fedi_data OWNER fedi_user;
EOSQL

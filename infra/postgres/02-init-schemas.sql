-- Garante que os schemas dos seus microsserviços existam
CREATE SCHEMA IF NOT EXISTS accounts;
CREATE SCHEMA IF NOT EXISTS catalogs;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS logs;

-- Se o usuário padrão não for o superuser, garante as permissões (opcional)
ALTER SCHEMA accounts OWNER TO atelie;
ALTER SCHEMA catalogs OWNER TO atelie;
ALTER SCHEMA orders OWNER TO atelie;
ALTER SCHEMA logs OWNER TO atelie;

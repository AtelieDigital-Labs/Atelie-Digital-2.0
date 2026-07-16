FROM alpine:latest

RUN apk add --no-cache docker-cli cronie

COPY infra/postgres/scripts /scripts
COPY infra/postgres/cron/root /etc/crontabs/root
COPY infra/postgres/cron/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && chmod +x /scripts/*.sh

ENTRYPOINT ["/entrypoint.sh"]
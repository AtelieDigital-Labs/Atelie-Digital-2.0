#!/bin/sh
set -e

echo "===== Cron Jobs ====="
cat /etc/crontabs/root

exec crond -f
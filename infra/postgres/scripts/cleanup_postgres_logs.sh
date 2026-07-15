#!/bin/bash

LOG_DIR="/var/lib/postgresql/data/log"

find "$LOG_DIR" -name "*.log" -mtime +7 -delete
find "$LOG_DIR" -name "*.json" -mtime +7 -delete

echo "Logs antigos removidos."
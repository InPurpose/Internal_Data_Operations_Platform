#!/bin/bash
# Usage: ./run_query.sh query.sql
# Runs SQL file on idop DB as stephenhuang

DB_USER="stephenhuang"
DB_NAME="idop"
HOST="localhost"  # Add if needed

if [ $# -ne 1 ]; then
  echo "Error: Exactly 1 argument (SQL filename) required."
  echo "Usage: $0 <sql_file.sql>"
  exit 1
fi

SQL_FILE="$1"

if [ ! -f "$SQL_FILE" ]; then
  echo "Error: File '$SQL_FILE' not found."
  exit 1
fi

psql -U "$DB_USER" -d "$DB_NAME" -h "$HOST" -f "$SQL_FILE" -t -A

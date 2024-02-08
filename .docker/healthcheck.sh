#!/bin/sh
set -e

# Check $MODE is set to "server"
# If true, check API server is running
if [ "$MODE" = "server" ]; then
  # curl "http://localhost:$PORT/v1/ping/"
  # check if answer is "ok"
  # if not, exit 1
  export ANSWER=$(curl -s "http://localhost:$PORT/v1/ping/")
  if [ "$ANSWER" = '"ok"' ]; then
    exit 0
  else
    exit 1
  fi
fi

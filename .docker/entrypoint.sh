#!/bin/sh
set -e

# Check $MODE is set to "server"
if [ "$MODE" = "server" ]; then
  python -m intape run -m -w $WORKERS -p $PORT -h $HOST
elif [ "$MODE" = "worker" ]; then
  python -m intape worker
else
  echo "ERROR: \$MODE is not set to \"server\" or \"worker\""
  exit 1
fi

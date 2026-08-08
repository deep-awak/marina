#!/bin/sh
set -eu

# On Render, this container is run as a Cron Job you trigger manually
# ("Trigger Run" in the dashboard) or on a schedule. The formula to
# solve is passed via the PROP environment variable.
#
# Locally, you can also just pass it as a normal docker argument,
# e.g.: docker run marina '(a&b | c)->d <-> ~e'

if [ "$#" -gt 0 ]; then
  exec /app/marina "$1"
fi

if [ -z "${PROP:-}" ]; then
  echo "Error: no formula provided." >&2
  echo "Set the PROP environment variable, or pass it as an argument." >&2
  echo "Example: PROP='(a&b | c)->d <-> ~e'" >&2
  exit 1
fi

exec /app/marina "$PROP"

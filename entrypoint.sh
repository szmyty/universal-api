#!/usr/bin/env bash
# ------------------------------------------------------------------
# Entry point script for the FastAPI service in a Docker container.
# ------------------------------------------------------------------
set -euo pipefail

# Main function to run the service
main() {
    # Update the CA certificates in the trust store
    printf "🔐 Updating certs in trust store...\n"
    update-ca-certificates

    # Start the FastAPI service using poetry
    printf "🚀 %s Starting FastAPI service...\n" "${APP_NAME:-project}"
    exec poetry run python -m fastapi run app/main.py \
        --host=0.0.0.0 \
        --port="${API_PORT:-8000}" \
        --no-reload \
        --proxy-headers \
        --root-path /api
}

main "$@"

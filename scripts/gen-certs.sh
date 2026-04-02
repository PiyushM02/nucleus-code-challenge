#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${ROOT}/certs"
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
  -keyout "${ROOT}/certs/server.key" \
  -out "${ROOT}/certs/server.crt" \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
echo "Created ${ROOT}/certs/server.crt and server.key"

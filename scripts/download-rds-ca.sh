#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
curl -o "$ROOT/global-bundle.pem" https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
echo "Certificado guardado en: $ROOT/global-bundle.pem"

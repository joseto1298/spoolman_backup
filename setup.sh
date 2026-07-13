#!/bin/bash
# Script de instalación para Spoolman Backup
set -e

VENV_DIR="$(dirname "$0")/venv"
PYTHON="$(which python3)"

echo "Creando entorno virtual..."
$PYTHON -m venv "$VENV_DIR"

echo "Instalando dependencias..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$(dirname "$0")/requirements.txt"

echo "Entorno virtual listo en: $VENV_DIR"
echo "Para activarlo: source $VENV_DIR/bin/activate"

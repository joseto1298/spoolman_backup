import os

SPOOLMAN_URL = os.environ.get("SPOOLMAN_URL", "http://localhost:7912/api/v1")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/home/pi/printer_data/config/spoolmanBackup/data.json")

try:
    TIMEOUT = int(os.environ.get("TIMEOUT", "30"))
except ValueError:
    TIMEOUT = 30

ENDPOINTS = ["spool", "material", "filament"]

# config.py
SPOOLMAN_URL = "http://localhost:7912/api/v1"  # URL de Spoolman
OUTPUT_PATH = "/home/pi/printer_data/config/spoolmanBackup/data.json"  # Fichero a sobrescribir
TIMEOUT = 30  # segundos para requests
ENDPOINTS = ["spool", "material" ,"filament"]

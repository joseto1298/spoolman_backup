#!/home/pi/spoolman_backup/venv/bin/python3
import os
import sys
import json

# Importamos configuración
try:
    from config import SPOOLMAN_URL, OUTPUT_PATH, TIMEOUT, ENDPOINTS
except ImportError as e:
    print(f"❌ Error al cargar config.py: {e}", file=sys.stderr)
    sys.exit(1)

def fetch_spoolman_data():
    """Obtiene datos de Spoolman"""
    data = {}
    for endpoint in ENDPOINTS:
        try:
            url = f"{SPOOLMAN_URL}/{endpoint}/"
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            json_data = response.json()
            # Si devuelve paginado, usamos 'results', si no devolvemos todo
            data[endpoint] = json_data.get("results", json_data) if isinstance(json_data, dict) else json_data
            #print(f"✅ {endpoint}: {len(data[endpoint])} registros")
        except Exception as e:
            print(f"❌ Error en {endpoint}: {e}", file=sys.stderr)
            data[endpoint] = []

    return data

def save_json(data, path):
    """Sobrescribe el fichero JSON existente"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    #print(f"💾 Datos guardados en {path}")

def main():
    data = fetch_spoolman_data()
    save_json(data, OUTPUT_PATH)

if __name__ == "__main__":
    main()

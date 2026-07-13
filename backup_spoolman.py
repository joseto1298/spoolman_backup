#!/home/pi/spoolman_backup/venv/bin/python3
import os
import sys
import json
import time
import logging
import requests

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

try:
    from config import SPOOLMAN_URL, OUTPUT_PATH, TIMEOUT, ENDPOINTS
except ImportError as e:
    logger.error("Error al cargar config.py: %s", e)
    sys.exit(1)


def fetch_with_retry(url, timeout, max_retries=3):
    """Realiza una petición GET con reintentos y backoff exponencial."""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (requests.ConnectionError, requests.Timeout) as e:
            wait = 2 ** (attempt - 1)
            logger.warning(
                "Intento %d/%d falló: %s. Reintentando en %ds...",
                attempt, max_retries, e, wait,
            )
            if attempt < max_retries:
                time.sleep(wait)
        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status and status >= 500 and attempt < max_retries:
                wait = 2 ** (attempt - 1)
                logger.warning(
                    "Intento %d/%d falló (HTTP %d): %s. Reintentando en %ds...",
                    attempt, max_retries, status, e, wait,
                )
                time.sleep(wait)
            else:
                logger.error("Error HTTP en %s: %s", url, e)
                return None
        except json.JSONDecodeError as e:
            logger.error("Respuesta no válida (JSON) en %s: %s", url, e)
            return None
    logger.error("Todos los reintentos fallaron para %s", url)
    return None


def fetch_spoolman_data():
    """Obtiene datos de Spoolman para cada endpoint configurado."""
    data = {}
    for endpoint in ENDPOINTS:
        url = f"{SPOOLMAN_URL}/{endpoint}/"
        json_data = fetch_with_retry(url, TIMEOUT)
        if json_data is None:
            data[endpoint] = []
        else:
            data[endpoint] = (
                json_data.get("results", json_data)
                if isinstance(json_data, dict)
                else json_data
            )
            logger.info("%s: %d registros", endpoint, len(data[endpoint]))
    return data


def save_json(data, path):
    """Guarda los datos en un fichero JSON, creando directorios si hace falta."""
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info("Datos guardados en %s", path)


def main():
    data = fetch_spoolman_data()
    save_json(data, OUTPUT_PATH)


if __name__ == "__main__":
    main()

# Spoolman Backup

Script de Python para respaldar datos de [Spoolman](https://github.com/Donkie/Spoolman) (gestor de filamentos para impresoras 3D) exportando los datos de su API a un fichero JSON.

## Sobre el proyecto

Spoolman Backup nació como herramienta personal para mantener una copia de seguridad de los datos de filamentos registrados en Spoolman. Está diseñado para ejecutarse de forma periódica en una Raspberry Pi junto a un servidor Klipper, aunque funciona en cualquier entorno con Python 3.

### ¿Qué guarda?

| Endpoint | Contenido |
|---|---|
| `spool` | Lotes de filamento registrados (peso, longitud, uso) |
| `material` | Tipos de material (PLA, PETG, ABS, etc.) |
| `filament` | Perfiles de filament (marca, diámetro, temperatura) |

El resultado es un único fichero JSON que puede importarse o consultarse fuera de Spoolman.

## Características

- Exporta datos de los endpoints `spool`, `material` y `filament`
- Reintentos automáticos con backoff exponencial (hasta 3 intentos)
- Logging estructurado con nivel configurable
- Configuración vía variables de entorno
- Soporte para respuestas paginadas de la API

## Instalación

```bash
git clone https://github.com/joseto1298/spoolman_backup.git
cd spoolman_backup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración

Las variables se pueden configurar en `config.py` o mediante variables de entorno:

| Variable | Por defecto | Descripción |
|---|---|---|
| `SPOOLMAN_URL` | `http://localhost:7912/api/v1` | URL base de la API de Spoolman |
| `OUTPUT_PATH` | `/home/pi/printer_data/config/spoolmanBackup/data.json` | Ruta del fichero JSON de salida |
| `TIMEOUT` | `30` | Timeout en segundos para las peticiones HTTP |
| `LOG_LEVEL` | `INFO` | Nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

Ejemplo con variables de entorno:

```bash
export SPOOLMAN_URL="http://192.168.1.100:7912/api/v1"
export OUTPUT_PATH="./backup/data.json"
export LOG_LEVEL="DEBUG"
```

## Uso

```bash
python backup_spoolman.py
```

## Ejecución automática (crontab)

Para ejecutar el backup automáticamente cada día a las 3:00 AM:

```bash
crontab -e
```

Agregar la linea:

```
0 3 * * * /home/pi/spoolman_backup/venv/bin/python /home/pi/spoolman_backup/backup_spoolman.py >> /home/pi/spoolman_backup/backup.log 2>&1
```

## Formato del JSON de salida

```json
{
    "spool": [...],
    "material": [...],
    "filament": [...]
}
```

## Integración con Moonraker

Este proyecto incluye un fichero `moonraker.conf` para gestionar actualizaciones desde la interfaz web. Copia el contenido en tu configuración de Moonraker:

```ini
[update_manager klipper-backup]
type: git_repo
path: /home/pi/spoolman_backup
origin: https://github.com/joseto1298/spoolman_backup
primary_branch: main
is_system_service: False
```

## Ejecución desde Klipper (G-code)

El fichero `spoolman_backup.cfg` define un comando G-code para ejecutar el backup directamente desde la impresora. Añade esto a tu configuración de Klipper:

```ini
[gcode_shell_command _BACKUP_SPOOLMAN]
# Realiza una copia de seguridad de la base de datos de Spoolman
command: /home/pi/spoolman_backup/venv/bin/python3 /home/pi/spoolman_backup/backup_spoolman.py
timeout: 30
verbose: True
```

Luego ejecuta desde la consola G-code:

```
_BACKUP_SPOOLMAN
```

## Licencia

MIT

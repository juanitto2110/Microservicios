from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import logging
import logging.handlers
import win32evtlogutil
import win32event
import win32evtlog
from functools import wraps
import win32security
import redis

# --- Logging Setup ---
# ... (same as before) ...

load_dotenv()
app = Flask(__name__)

# --- Authentication Setup ---
# ... (same as before) ...
# --- End of Authentication Setup ---

# --- Redis Setup ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    cache.ping()  
    logger.info("Conexión con Redis establecida exitosamente.")
except Exception as e:
    logger.error(f"Error al conectar con Redis: {e}")
    cache = None  
# --- End of Redis Setup ---

# --- Configuration Service ---
class ConfigService:
    def __init__(self, cache_client):
        self.cache = cache_client

    def get_config(self, key, default=None):
        """Retrieves a configuration value from Redis."""
        if self.cache is None:
            logger.warning(f"Redis no disponible. Usando valor por defecto para {key}.")
            return default

        value = self.cache.get(key)
        if value is None:
            logger.warning(f"Clave de configuración no encontrada: {key}. Usando valor por defecto.")
            return default
        return value.decode("utf-8")  # Decode from bytes to string

    def set_config(self, key, value):
        """Sets a configuration value in Redis."""
        if self.cache is None:
            logger.warning(f"Redis no disponible. No se puede establecer el valor para {key}.")
            return

        self.cache.set(key, value)

config_service = ConfigService(cache)  # Create the configuration service instance
# --- End of Configuration Service ---

# --- Example: Load Configuration from Redis ---
SERVICE_NAME = config_service.get_config("SERVICE_NAME", "Servicio de Usuarios") 
# ... load other configurations using config_service.get_config(...) ...
# --- End of Example ---

# Simulated database
usuarios = [
    {"id": 1, "nombre": "Ana", "email": "ana@ejemplo.com"},
    {"id": 2, "nombre": "Berto", "email": "berto@ejemplo.com"},
]

# --- Caching Decorator ---
# ... (same as before) ...
# --- End of Caching Decorator ---

# --- Routes ---
@app.route("/api/usuarios", methods=["GET"])
@requires_auth
@cached
def obtener_usuarios():
    logger.info("Solicitud recibida: GET /api/usuarios")
    return jsonify({"servicio": SERVICE_NAME, "data": usuarios, "status": "success"}) # Using configured service name

@app.route("/api/usuarios/<int:usuario_id>", methods=["GET"])
@requires_auth
@cached
def obtener_usuario(usuario_id):
    # ... (same as before) ... 

@app.route("/api/usuarios/healthcheck", methods=["GET"])
def healthcheck():
    # ... (same as before) ...

# --- End of Routes --- 

if __name__ == "__main__":
    # ... (same as before) ... 
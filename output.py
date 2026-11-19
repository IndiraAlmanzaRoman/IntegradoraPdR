import json
import socket
import random
import datetime
import platform
import platform
import subprocess
import re


salida = "Llamado desde MiDispositivo.py"


ARCHIVO_LOG = "network_logs.jsonl"


def obtener_ip_local():
    """
    Obtiene la dirección IP local del equipo actual.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-05

    Parámetros: Ninguno.

    Salida: str: Dirección IP local activa del equipo.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def obtener_gateway_red():
    """
    Obtiene la puerta de enlace predeterminada del sistema.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-05

    Parámetros:
    Ninguno.

    Salida:
    str: Dirección IP del gateway o 'No disponible'.
    """
    sistema = platform.system().lower()

    try:
        if sistema == "darwin":
            salida = subprocess.check_output(["route", "-n", "get", "default"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"gateway:\s+([0-9.]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "linux":
            for comando in (["ip", "route", "show", "default"], ["route", "-n"]):
                try:
                    salida = subprocess.check_output(comando, text=True, stderr=subprocess.STDOUT)
                    coincidencia = re.search(r"(?:default|0\.0\.0\.0)\s+([0-9.]+)", salida)
                    if coincidencia:
                        return coincidencia.group(1)
                except Exception:
                    continue

        elif sistema == "windows":
            salida = subprocess.check_output(["ipconfig"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"Predeterminado.*?:\s*([0-9.]+)", salida, re.IGNORECASE)
            if coincidencia:
                return coincidencia.group(1)
    except Exception:
        pass

    return "No disponible"


def obtener_mac_red():
    """
    Obtiene la dirección MAC de la interfaz de red principal.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-05

    Parámetros:
    Ninguno.

    Salida:
    str: Dirección MAC de la red o 'No disponible'.
    """
    sistema = platform.system().lower()

    try:
        if sistema == "darwin":
            salida = subprocess.check_output(["ifconfig", "-a"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"ether\s+([0-9A-Fa-f:]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "linux":
            salida = subprocess.check_output(["ip", "link"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"link/ether\s+([0-9A-Fa-f:]+)", salida)
            if coincidencia:
                return coincidencia.group(1)

        elif sistema == "windows":
            salida = subprocess.check_output(["ipconfig", "/all"], text=True, stderr=subprocess.STDOUT)
            coincidencia = re.search(r"Direcci[oó]n\s+f[ií]sica.*?:\s*([0-9A-Fa-f-]+)", salida)
            if coincidencia:
                return coincidencia.group(1)
    except Exception:
        pass

    return "No disponible"


def obtener_info_red():
    """
    Reúne la información de red más relevante del equipo.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-05

    Parámetros:
    Ninguno.

    Salida:
    dict: Diccionario con hostname, IP local, gateway y MAC.
    """
    #Output
    print("Obteniendo información de la red...")
    return {
        "hostname": socket.gethostname(),
        "ip_local": obtener_ip_local(),
        "gateway": obtener_gateway_red(),
        "mac_address": obtener_mac_red(),
        "sistema_operativo": platform.system(),
        "version_sistema": platform.release()
    }


def crear_evento_red(ip_origen, ip_destino):
    """
    Crea un diccionario que representa un evento de red con datos simulados.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-01

    Parámetros:
    ip_origen (str): Dirección IP de la máquina que envía los datos.
    ip_destino (str): Dirección IP del servidor o equipo de destino.

    Salida:
    dict: Diccionario con la información detallada del evento registrado.
    """
    puertos_comunes = [80, 443, 22, 53, 8080]
    estados = ["PERMITIDO", "BLOQUEADO", "SOSPECHOSO"]
    protocolos = ["TCP", "UDP"]
    usuarios = ["Ramona", "Indira", "Said"]

    evento = {
        "timestamp": datetime.now().isoformat(),
        "ip_origen": ip_origen,
        "ip_destino": ip_destino,
        "puerto_destino": random.choice(puertos_comunes),
        "protocolo": random.choice(protocolos),
        "bytes_enviados": random.randint(64, 4096),
        "estado": random.choice(estados),
        "usuario": random.choice(usuarios)
    }
    return evento


def guardar_log_jsonl(evento, nombre_archivo=ARCHIVO_LOG):
    """
    Convierte un diccionario de evento en una línea JSON y la añade al archivo.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-01

    Parámetros:
    evento (dict): Diccionario con el evento que se va a registrar.
    nombre_archivo (str): Nombre del archivo .jsonl donde se guardará.

    Salida:
    bool: True si la escritura fue exitosa, False en caso de error.
    """
    try:
        with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
            linea_json = json.dumps(evento, ensure_ascii=False)
            archivo.write(linea_json + '\n')
        return True
    except Exception as e:
        print(f"Error al guardar el log: {e}")
    return False

def obtener_info_red():
    """
    Reúne la información de red más relevante del equipo.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-05

    Parámetros:
    Ninguno.

    Salida:
    dict: Diccionario con hostname, IP local, gateway y MAC.
    """
    #Output
    print("Obteniendo información de la red...")
    return {
        "hostname": socket.gethostname(),
        "ip_local": obtener_ip_local(),
        "gateway": obtener_gateway_red(),
        "mac_address": obtener_mac_red(),
        "sistema_operativo": platform.system(),
        "version_sistema": platform.release()
    }


    

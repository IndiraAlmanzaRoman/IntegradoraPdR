import json
import random
import re
import socket
import subprocess
import platform
from datetime import datetime
from flask import Flask, app, render_template, request, json, jsonify

app = Flask(__name__)



ARCHIVO_LOG = "network_logs.jsonl"

def leer_logs_bloqueados(nombre_archivo=ARCHIVO_LOG):
    """
    Lee un archivo JSONL y muestra los eventos cuya red fue bloqueada.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-06

    Parámetros:
    nombre_archivo (str): Nombre del archivo .jsonl a revisar.

    Salida:
    list: Lista de eventos bloqueados.
    """
    registros_bloqueados = []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                evento = json.loads(linea)
                if evento.get("estado") == "BLOQUEADO":
                    registros_bloqueados.append(evento)
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe todavía.")
        return []

    print("=== EVENTOS BLOQUEADOS ===")
    if not registros_bloqueados:
        print("No hay eventos bloqueados.")
    else:
        for evento in registros_bloqueados:
            print(evento)

    return registros_bloqueados

def leer_logs_no_bloqueados(nombre_archivo=ARCHIVO_LOG):
    """
    Lee un archivo JSONL y muestra los eventos cuya red NO fue bloqueada.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-06

    Parámetros:
    nombre_archivo (str): Nombre del archivo .jsonl a revisar.

    Salida:
    list: Lista de eventos NO bloqueados.
    """
    registros_no_bloqueados = []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                evento = json.loads(linea)
                if evento.get("estado") == "SOSPECHOSO" | "PERMITIDO":
                    registros_no_bloqueados.append(evento)
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe todavía.")
        return []

    print("=== EVENTOS NO BLOQUEADOS ===")
    if not registros_no_bloqueados:
        print("No hay eventos no bloqueados.")
    else:
        for evento in registros_no_bloqueados:
            print(evento)

    return registros_no_bloqueados

def leer_logs_todos(nombre_archivo=ARCHIVO_LOG):
    """
    Lee un archivo JSONL y muestra TODOS los eventos.

    Autor: Indira Almanza Roman
    Fecha de creación: 2026-11-06

    Parámetros:
    nombre_archivo (str): Nombre del archivo .jsonl a revisar.

    Salida:
    list: Lista de eventos bloqueados.
    """
    registros_todos = []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                evento = json.loads(linea)
                registros_todos.append(evento)
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe todavía.")
        return []

    print("=== EVENTOS ===")
    if not registros_todos:
        print("No hay eventos.")
    else:
        for evento in registros_todos:
            print(evento)

    return registros_todos


@app.route('/', methods=['GET'])
def manejar_html():
    mostrar_logs_bloqueados = mostrar_logs_bloqueados()
    leer_logs_bloqueados = leer_logs_bloqueados()
    leer_logs_todos = leer_logs_todos()

    return render_template('templates'/'html'/'views'/'incidentes'/'incidentes.html', mostrar_logs_bloqueados = mostrar_logs_bloqueados, leer_logs_bloqueados = leer_logs_bloqueados, leer_logs_todos = leer_logs_todos)

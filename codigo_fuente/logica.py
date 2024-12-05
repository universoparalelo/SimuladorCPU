import json
import csv
import copy

# Constantes
QUANTO = 3
MEMORIA_PRINCIPAL = {
    1: {'dir_inicial': 0, 'tamanio': 250000, 'proceso': 0, 'estado': 'libre', 'fr_interna': 0},
    2: {'dir_inicial': 250000, 'tamanio': 150000, 'proceso': 0, 'estado': 'libre', 'fr_interna': 0},
    3: {'dir_inicial': 400000, 'tamanio': 50000, 'proceso': 0, 'estado': 'libre', 'fr_interna': 0}
}

def leer_json(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        return json.load(json_file)

def convertir_valor(valor):
    try:
        return int(valor)
    except ValueError:
        try:
            return float(valor)
        except ValueError:
            return valor

def leer_csv(csv_file_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row = {key: convertir_valor(value) for key, value in row.items()}
            data.append(row)
    return data

def obtener_datos(file_path):
    if file_path.endswith('.json'):
        return leer_json(file_path)
    elif file_path.endswith('.csv'):
        return leer_csv(file_path)
    else:
        raise ValueError("Formato de archivo no soportado. Usa JSON o CSV.")

def ordenar_datos(datos):
    datos = [proceso for proceso in datos if proceso['tamanio'] <= 250000]
    for proceso in datos:
        proceso['tiempo_irrupcion_constante'] = proceso['tiempo_irrupcion']
    return sorted(datos, key=lambda x: x['tiempo_arribo'])

def actualizar_estado_memoria(particion, proceso, liberar=False):
    if liberar:
        MEMORIA_PRINCIPAL[particion].update({'proceso': 0, 'estado': 'libre', 'fr_interna': 0})
    else:
        MEMORIA_PRINCIPAL[particion].update({
            'proceso': proceso['proceso_id'],
            'estado': 'ocupado',
            'fr_interna': MEMORIA_PRINCIPAL[particion]['tamanio'] - proceso['tamanio']
        })

def worstFit(proceso):
    tamanio_proceso = proceso['tamanio']
    max_fr_int = -999
    particion = 0

    for key, value in MEMORIA_PRINCIPAL.items():
        if value['estado'] == 'libre' and value['tamanio'] - tamanio_proceso >= max_fr_int:
            max_fr_int = value['tamanio'] - tamanio_proceso
            particion = key

    return particion

def asignar_proceso_a_memoria(proceso, cola_listos, cola_listos_suspendidos, suspendido=False):
    particion = worstFit(proceso)
    if particion == 0 and len(cola_listos_suspendidos) < 2 and proceso not in cola_listos_suspendidos:
        proceso['estado'] = 'suspendido'
        cola_listos_suspendidos.append(proceso)
    elif particion:
        proceso['estado'] = 'listo'
        cola_listos.append(proceso)
        if suspendido:
            cola_listos_suspendidos.remove(proceso)
        actualizar_estado_memoria(particion, proceso)

def agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general):
    for proceso in procesos_ordenados:
        if proceso['estado'] == 'nuevo' and proceso['tiempo_arribo'] <= tiempo_general:
            if len(cola_listos) < 3:
                asignar_proceso_a_memoria(proceso, cola_listos, cola_listos_suspendidos)
            elif len(cola_listos_suspendidos) < 2:
                proceso['estado'] = 'suspendido'
                cola_listos_suspendidos.append(proceso)

def asignarMemoria(procesos_ordenados):
    cola_listos = []
    cola_listos_suspendidos = []
    cola_terminados = []
    tiempo_general = 0
    tiempos = []
    historial = []

    agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)

    while len(procesos_ordenados) != len(cola_terminados):
        while len(cola_listos) == 0:
            tiempo_general += QUANTO
            agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)

        # sacar proceso de cola_listos y llevarlo a ejecucion
        proceso = cola_listos.pop(0)
        proceso['estado'] = 'ejecucion'
        historial.append((tiempo_general, list(cola_listos), list(cola_listos_suspendidos), list(cola_terminados), proceso, copy.deepcopy(MEMORIA_PRINCIPAL)))

        if proceso['tiempo_irrupcion'] <= QUANTO:
            tiempo_general += proceso['tiempo_irrupcion']
            tiempo_retorno = tiempo_general - proceso['tiempo_arribo']
            tiempos.append({
                'proceso': proceso['proceso_id'],
                'tiempo_retorno': tiempo_retorno,
                'tiempo_espera': tiempo_retorno - proceso['tiempo_irrupcion_constante']
            })
            particion = next((key for key, value in MEMORIA_PRINCIPAL.items() if value['proceso'] == proceso['proceso_id']), 0)
            actualizar_estado_memoria(particion, proceso, liberar=True)
            proceso['estado'] = 'terminado'
            cola_terminados.append(proceso)

            if cola_listos_suspendidos:
                asignar_proceso_a_memoria(cola_listos_suspendidos[0], cola_listos, cola_listos_suspendidos, suspendido=True)
        else:
            tiempo_general += QUANTO
            proceso['tiempo_irrupcion'] -= QUANTO
            cola_listos.append(proceso)

        agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)

    return tiempos, historial, tiempo_general

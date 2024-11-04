import json
import time
import csv

# Constantes
QUANTO = 3
MEMORIA_PRINCIPAL = { 
       1: {
        'dir_inicial': 0,
        'tamanio': 250000,
        'proceso': 0,
        'estado': 'libre',
        'fr_interna': 0
    }, 2: {
        'dir_inicial': 250000,
        'tamanio': 150000,
        'proceso': 0,
        'estado': 'libre',
        'fr_interna': 0
    }, 3: {
        'dir_inicial': 400000,
        'tamanio': 50000,
        'proceso': 0,
        'estado': 'libre',
        'fr_interna': 0
    }}


def leer_json(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def leer_csv(csv_file_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
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
    return sorted(datos, key=lambda x: x['tiempo_arribo'])

# def crearCronogramaRR(datos_ordenados):
#     tiempo_general = 0
#     var_corte = 0 
#     cronograma = {}

#     while var_corte < len(datos_ordenados):
        
#         for proceso in datos_ordenados:
#             if proceso['tiempo_arribo'] <= tiempo_general:
#                 if proceso['tiempo_irrupcion'] != 0:
#                     cronograma[tiempo_general] = proceso.copy()
#                     if proceso['tiempo_irrupcion'] <= QUANTO:
#                         tiempo_general += proceso['tiempo_irrupcion']
#                         proceso['tiempo_irrupcion'] = 0
#                         var_corte += 1
#                     else:
#                         proceso['tiempo_irrupcion'] -= QUANTO
#                         tiempo_general += QUANTO    
    # return cronograma

def asignarMemoria(procesos_ordenados):
    # claves = list(procesos_ordenados)
    i = 0
    cola_listos = []
    cola_listos_suspendidos = []
    cola_terminados = []
    tiempo_general = 0
    tiempos = []

    while (len(cola_terminados) < 10):

        # agregamos procesos a cola de listos o a cola de listos y suspendidos
        for proceso in procesos_ordenados:
            if proceso['estado']=='nuevo' and proceso['tiempo_arribo'] <= tiempo_general:
                if len(cola_listos) < 3:
                    asignado = worstFit(proceso)
                    if asignado == 0:
                        if len(cola_listos_suspendidos) < 2:
                            cola_listos_suspendidos.append(proceso)
                            proceso['estado'] = 'suspendido'
                    else:
                        cola_listos.append(proceso)
                        proceso['estado'] = 'listo'
                        MEMORIA_PRINCIPAL[asignado]['proceso'] = proceso['proceso_id']
                        MEMORIA_PRINCIPAL[asignado]['fr_interna'] = MEMORIA_PRINCIPAL[asignado]['tamanio'] - proceso['tamanio']
                        MEMORIA_PRINCIPAL[asignado]['estado'] = 'ocupado'
                       
                elif len(cola_listos_suspendidos) < 2:
                    cola_listos_suspendidos.append(proceso)
                    proceso['estado'] = 'suspendido'

            else:
                break
        
        # sacar procesos de procesos_ordenados que ya estan en cola_listos y cola_listos_suspendidos
        for proceso in procesos_ordenados:
            if proceso in cola_listos or proceso in cola_listos_suspendidos:
                procesos_ordenados.remove(proceso)


        # ejecutar procesos en cola_listos
        for proceso in cola_listos:
            print('====================================================================')
            print('Tiempo general: ', tiempo_general)
            print('Cola de listos: ', cola_listos)
            print('Cola de listos suspendidos: ', cola_listos_suspendidos)
            imprimirMP()
            print('Cola de terminados: ', cola_terminados)
            print('Proceso en ejecucion: ', proceso['proceso_id'])
            print('====================================================================')

            if proceso['tiempo_irrupcion'] <= QUANTO:
                tiempo_general += proceso['tiempo_irrupcion']
                tiempo_retorno = tiempo_general - proceso['tiempo_arribo']
                tiempos.append({
                    'proceso': proceso['proceso_id'],
                    'tiempo_retorno': tiempo_retorno,
                    'tiempo_espera': tiempo_retorno - proceso['tiempo_irrupcion']
                })
                # buscar particion del proceso
                particion = 0
                for key, value in MEMORIA_PRINCIPAL.items():
                    if value['proceso'] == proceso['proceso_id']:
                        particion = key
                        break

                # libero memoria
                MEMORIA_PRINCIPAL[particion]['estado'] = 'libre'
                MEMORIA_PRINCIPAL[particion]['proceso'] = 0
                MEMORIA_PRINCIPAL[particion]['fr_interna'] = 0
                cola_listos.remove(proceso)
                cola_terminados.append(proceso)

                # pregunto por la cola de listos suspendidos
                if len(cola_listos_suspendidos) > 0:
                    nuevo_proceso = cola_listos_suspendidos[0]
                    asignado = worstFit(nuevo_proceso)
                    if asignado == 0:
                        continue
                    else:
                        cola_listos.append(nuevo_proceso)
                        nuevo_proceso['estado'] = 'listo'
                        MEMORIA_PRINCIPAL[asignado]['proceso'] = nuevo_proceso['proceso_id']
                        MEMORIA_PRINCIPAL[asignado]['fr_interna'] = MEMORIA_PRINCIPAL[asignado]['tamanio'] - nuevo_proceso['tamanio']
                        MEMORIA_PRINCIPAL[asignado]['estado'] = 'ocupado'
                        print(cola_listos_suspendidos, proceso)
                        cola_listos_suspendidos.remove(nuevo_proceso)

            else:
                tiempo_general += QUANTO
                proceso['tiempo_irrupcion'] -= QUANTO

        
        input('Presiona enter para continuar...')
    imprimirTiempos(tiempos, tiempo_general)
        

def worstFit(proceso):
    tamanio_proceso = proceso['tamanio']
    max_fr_int = -999
    particion = 0

    for key, value in MEMORIA_PRINCIPAL.items():
        if value['estado'] == 'libre' and value['tamanio'] - tamanio_proceso >= max_fr_int:
            max_fr_int = value['tamanio'] - tamanio_proceso
            particion = key
            
    return particion

def imprimirMP():
    print('Memoria principal: ')
    for key, value in MEMORIA_PRINCIPAL.items():
        print(key, value)

def imprimirTiempos(tiempos, tiempo_total):
    print('------------------------------------------------------------')
    print('Tiempo de retorno y espera de cada proceso: ')
    print('Proceso | Tiempo de retorno | Tiempo de espera')
    for tiempo in tiempos:
        print(tiempo['proceso'], ' | ', tiempo['tiempo_retorno'], ' | ', tiempo['tiempo_espera'])
    
    tiempo_retorno_promedio = sum([tiempo['tiempo_retorno'] for tiempo in tiempos]) / len(tiempos)
    tiempo_espera_promedio = sum([tiempo['tiempo_espera'] for tiempo in tiempos]) / len(tiempos)
    print('Tiempo de retorno promedio: ', tiempo_retorno_promedio)
    print('Tiempo de espera promedio: ', tiempo_espera_promedio)
    rendimiento = len(tiempos) / tiempo_total
    print('Rendimiento: ', rendimiento)
    print('--------------------------------------------------------------')

def imprimirDatos(datos):
    print('Procesos: ')
    for key, value in datos.items():
        print(key, value)


#######################################################
# Obteniedo datos de un archivo
datos = obtener_datos('procesos.json')

# Ordenando datos segun tiempo de arribo
datos_ordenados = ordenar_datos(datos)

# Procesando cronograma
asignarMemoria(datos_ordenados)





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
        'estado': 'libre'
    }, 2: {
        'dir_inicial': 250000,
        'tamanio': 150000,
        'proceso': 0,
        'estado': 'libre'
    }, 3: {
        'dir_inicial': 400000,
        'tamanio': 50000,
        'proceso': 0,
        'estado': 'libre'
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

def crearCronogramaRR(datos_ordenados):
    tiempo_general = 0
    var_corte = 0 
    cronograma = {}

    while var_corte < len(datos_ordenados):
        
        for proceso in datos_ordenados:
            if proceso['tiempo_arribo'] <= tiempo_general:
                if proceso['tiempo_irrupcion'] != 0:
                    cronograma[tiempo_general] = proceso.copy()
                    if proceso['tiempo_irrupcion'] <= QUANTO:
                        tiempo_general += proceso['tiempo_irrupcion']
                        proceso['tiempo_irrupcion'] = 0
                        var_corte += 1
                    else:
                        proceso['tiempo_irrupcion'] -= QUANTO
                        tiempo_general += QUANTO
            
        
    return cronograma

def asignarMemoria(cronograma):
    claves = list(cronograma.keys())
    i = 0
    cola_listos = []
    cola_listos_bloqueados = []
    cola_terminados = []
    tiempo_general = claves[0]
    ultimo_valor = 0
    tiempos = []

    while (len(cola_terminados) < 10):
        print('====================================================================')
        print('Tiempo general: ', tiempo_general)
        proceso_en_ejecucion = cronograma[claves[i]]

        # agregamos procesos a cola de listos o a cola de listos y bloqueados
        for j in range(ultimo_valor, len(cronograma)):
            if cronograma[claves[j]]['estado']=='nuevo' and cronograma[claves[j]]['tiempo_arribo'] <= tiempo_general:
                if len(cola_listos) < 3:
                    cola_listos.append(cronograma[claves[j]])
                    cronograma[claves[j]]['estado'] = 'listo'
                    ultimo_valor += 1
                    
                # elif len(cola_listos_bloqueados) < 2:
                #     cola_listos_bloqueados.append(cronograma[claves[j]])
                #     cronograma[claves[j]]['estado'] = 'bloqueado'
                #     ultimo_valor += 1

            else:
                break

        
        # nos fijamos si el primer proceso puede ser asignado a una particion en memoria
        # voy a repetir codigo, optimizar mas adelante !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        while len(cola_listos) > 0:
            asignado = worstFit(cola_listos[0])
            if asignado == 0:
                break
            else:
                MEMORIA_PRINCIPAL[asignado]['proceso'] = cola_listos[0]['proceso_id']
                MEMORIA_PRINCIPAL[asignado]['estado'] = 'ocupado'
                cola_listos.pop(0)
        
        print('Cola de listos: ', cola_listos)
        print('Cola de listos bloqueados: ', cola_listos_bloqueados)
        imprimirMP()
        print('Cola de terminados: ', cola_terminados)

        # chequeamos que el proceso en ejecucion este asignado en memoria
        esta_en_mp = False
        for particion in MEMORIA_PRINCIPAL:
            if MEMORIA_PRINCIPAL[particion]['proceso'] == proceso_en_ejecucion['proceso_id']:
                esta_en_mp = True
                MEMORIA_PRINCIPAL[particion]['estado'] = 'libre'
                MEMORIA_PRINCIPAL[particion]['proceso'] = 0
                break
        
        print('Proceso en ejecucion: ', proceso_en_ejecucion['proceso_id'])
        if esta_en_mp:
            i += 1
            if proceso_en_ejecucion['tiempo_irrupcion'] - QUANTO <= 0:
                cola_terminados.append(proceso_en_ejecucion['proceso_id'])
                tiempo_general += proceso_en_ejecucion['tiempo_irrupcion']
                tiempo_retorno = tiempo_general - proceso_en_ejecucion['tiempo_arribo']
                tiempos.append({
                    'proceso': proceso_en_ejecucion['proceso_id'],
                    'tiempo_retorno': tiempo_retorno,
                    'tiempo_espera': tiempo_retorno - proceso_en_ejecucion['tiempo_irrupcion']
                })
                # del cronograma[claves[0]]
            else:
                tiempo_general += QUANTO
        
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

# Creando cronograma de ejecucion
cronograma = crearCronogramaRR(datos_ordenados)

# Procesando cronograma
asignarMemoria(cronograma)





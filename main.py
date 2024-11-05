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

def actualizar_estado_memoria(particion, proceso, liberar=False):
    if liberar:
        MEMORIA_PRINCIPAL[particion].update({'proceso': 0, 'estado': 'libre', 'fr_interna': 0})
    else:
        MEMORIA_PRINCIPAL[particion].update({
            'proceso': proceso['proceso_id'],
            'estado': 'ocupado',
            'fr_interna': MEMORIA_PRINCIPAL[particion]['tamanio'] - proceso['tamanio']
        })

def asignar_proceso_a_memoria(proceso, cola_listos, cola_listos_suspendidos):
    particion = worstFit(proceso)
    if particion == 0 and len(cola_listos_suspendidos) < 2:
        proceso['estado'] = 'suspendido'
        cola_listos_suspendidos.append(proceso)
    elif particion:
        proceso['estado'] = 'listo'
        cola_listos.append(proceso)
        actualizar_estado_memoria(particion, proceso)

def asignarMemoria(procesos_ordenados):
    cola_listos = []
    cola_listos_suspendidos = []
    cola_terminados = []
    tiempo_general = 0
    tiempos = []

    for proceso in list(procesos_ordenados):  # Usamos una copia para modificar el original
        # Revisamos y asignamos procesos
        for proceso in procesos_ordenados: 
            if proceso['estado'] == 'nuevo' and proceso['tiempo_arribo'] <= tiempo_general:
                if len(cola_listos) < 3:
                    asignar_proceso_a_memoria(proceso, cola_listos, cola_listos_suspendidos)
                elif len(cola_listos_suspendidos) < 2:
                    proceso['estado'] = 'suspendido'
                    cola_listos_suspendidos.append(proceso)
                
                procesos_ordenados.remove(proceso)

         # sacar procesos de procesos_ordenados que ya estan en cola_listos y cola_listos_suspendidos
        #for proceso in procesos_ordenados:
         #   if proceso in cola_listos or proceso in cola_listos_suspendidos:
          #      procesos_ordenados.remove(proceso)

        for proceso in cola_listos[:]:  # Itera sobre una copia para modificar la cola en ejecución
            tiempo_anterior = tiempo_general
            ejecutar_proceso(proceso, cola_listos, cola_listos_suspendidos, cola_terminados, tiempos, tiempo_general)
            tiempo_general += min(QUANTO, proceso['tiempo_irrupcion']) - tiempo_anterior
        
        # Mover procesos de suspendidos a listos si hay espacio
        while len(cola_listos) < 3 and cola_listos_suspendidos:
            proceso_suspendido = cola_listos_suspendidos.pop(0)
            proceso_suspendido['estado'] = 'listo'
            asignar_proceso_a_memoria(proceso_suspendido, cola_listos, cola_listos_suspendidos)

        # Pausa para continuar
        print("Estado actual de la simulación. Presiona enter para continuar...")
        input()
    
    imprimirTiempos(tiempos, tiempo_general)

# Ejecutar procesos
def ejecutar_proceso(proceso, cola_listos, cola_listos_suspendidos, cola_terminados, tiempos, tiempo_general):
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
        actualizar_estado_memoria(particion, proceso, liberar=True)
        cola_listos.remove(proceso)
        cola_terminados.append(proceso)
        if cola_listos_suspendidos:
            asignar_proceso_a_memoria(cola_listos_suspendidos[0], cola_listos, cola_listos_suspendidos)
    else:
        tiempo_general += QUANTO
        proceso['tiempo_irrupcion'] -= QUANTO      

# Algoritmo de asignación Worst Fit
def worstFit(proceso):
    tamanio_proceso = proceso['tamanio']
    particion, max_fr_int = 0, -1
    
    for key, value in MEMORIA_PRINCIPAL.items():
        fr_interna = value['tamanio'] - tamanio_proceso
        if value['estado'] == 'libre' and fr_interna >= max_fr_int:
            max_fr_int, particion = fr_interna, key
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

# def imprimirDatos(datos):
#     print('Procesos: ')
#     for key, value in datos.items():
#         print(key, value)


#######################################################
# Obteniedo datos de un archivo
datos = obtener_datos(r'C:\Users\ACER\Desktop\TPI_SO\SimuladorCPU\procesos.json')

# Ordenando datos segun tiempo de arribo
datos_ordenados = ordenar_datos(datos)

# Procesando cronograma
asignarMemoria(datos_ordenados)





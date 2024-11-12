import json
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


def asignarMemoria(procesos_ordenados):
    cola_listos = []
    cola_listos_suspendidos = []
    cola_terminados = []
    tiempo_general = 0
    tiempos = []

    # agregamos procesos a cola de listos o a cola de listos y suspendidos
    agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)
    

    while (len(cola_listos) > 0):
        # ejecutar procesos en cola_listos
        for proceso in cola_listos:
            impresionParcial(tiempo_general, cola_listos, cola_listos_suspendidos, cola_terminados, proceso)

            # el proceso ya termino de ejecutarse entonces liberamos memoria y lo pasamos a cola de terminados
            # aniadimos un proceso de la cola de listos suspendidos a la cola de listos SI ES POSIBLE
            if proceso['tiempo_irrupcion'] <= QUANTO:
                tiempo_general += proceso['tiempo_irrupcion']
                tiempo_retorno = tiempo_general - proceso['tiempo_arribo']
                tiempos.append({
                    'proceso': proceso['proceso_id'],
                    'tiempo_retorno': tiempo_retorno,
                    'tiempo_espera': tiempo_retorno - proceso['tiempo_irrupcion_constante']
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
                    for proceso2 in cola_listos_suspendidos:
                        asignado = worstFit(proceso2)
                        if asignado != 0:
                            cola_listos.append(proceso2)
                            cola_listos_suspendidos.remove(proceso2)
                            proceso2['estado'] = 'listo'
                            MEMORIA_PRINCIPAL[asignado]['proceso'] = proceso2['proceso_id']
                            MEMORIA_PRINCIPAL[asignado]['fr_interna'] = MEMORIA_PRINCIPAL[asignado]['tamanio'] - proceso2['tamanio']
                            MEMORIA_PRINCIPAL[asignado]['estado'] = 'ocupado'
                            break

            else:
                tiempo_general += QUANTO
                proceso['tiempo_irrupcion'] -= QUANTO
                
            agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)
        
    imprimirTiempos(tiempos, tiempo_general)


def limpiarProcesosOrdenados(procesos_ordenados, cola_listos, cola_listos_suspendidos):
    i = 0

    while i < len(procesos_ordenados):
        if procesos_ordenados[i] in cola_listos or procesos_ordenados[i] in cola_listos_suspendidos:
            procesos_ordenados.remove(procesos_ordenados[i])
        else:
            i += 1


def agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general):

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
    limpiarProcesosOrdenados(procesos_ordenados, cola_listos, cola_listos_suspendidos)


def worstFit(proceso):
    tamanio_proceso = proceso['tamanio']
    max_fr_int = -999
    particion = 0

    for key, value in MEMORIA_PRINCIPAL.items():
        if value['estado'] == 'libre' and value['tamanio'] - tamanio_proceso >= max_fr_int:
            max_fr_int = value['tamanio'] - tamanio_proceso
            particion = key
            
    return particion


def impresionParcial(tiempo_general, cola_listos, cola_listos_suspendidos, cola_terminados, proceso):
    print('====================================================================')
    print('Tiempo general: ', tiempo_general)
    print('Cola de listos: ', end="")
    for proceso2 in cola_listos: print(proceso2['proceso_id'], end=" ")
    print('\nCola de listos suspendidos: ', end="")
    for proceso3 in cola_listos_suspendidos: print(proceso3['proceso_id'], end=" ")
    imprimirMP()
    print('\nCola de terminados: ', end="")
    for proceso4 in cola_terminados: print(proceso4['proceso_id'], end=" ")
    print('\nProceso en ejecucion: ', proceso['proceso_id'])
    print('====================================================================')
    input('Presiona enter para continuar...')


def imprimirMP():
    print('\nMemoria principal: ')
    valores = MEMORIA_PRINCIPAL[1].keys()
    for valor in valores:
        print(valor, end=" | ")
    
    for key, value in MEMORIA_PRINCIPAL.items():
        print(f"\n{key}", end=" | ")
        for v in value.values():
            print(v, end=" | ")


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





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


def convertir_valor(valor):
    """Intenta convertir el valor a int o float, si es posible."""
    try:
        # Intenta convertir a entero
        return int(valor)
    except ValueError:
        try:
            # Intenta convertir a decimal (float)
            return float(valor)
        except ValueError:
            # Si no se puede convertir, retorna el valor original (string)
            return valor


def leer_csv(csv_file_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Convierte cada valor del diccionario usando la función `convertir_valor`
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
    # Agregar el nuevo atributo a cada proceso
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


def asignarMemoria(procesos_ordenados):
    cola_listos = []
    cola_listos_suspendidos = []
    cola_terminados = []
    tiempo_general = 0
    tiempos = []
    cantidad_procesos = len(procesos_ordenados)

    # agregamos procesos a cola de listos o a cola de listos y suspendidos
    agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)
    

    while (len(cola_listos) > 0):
        # ejecutar procesos en cola_listos
        # for proceso in cola_listos:
        proceso = cola_listos[0]

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

            actualizar_estado_memoria(particion, proceso, liberar=True)
            cola_listos.remove(proceso)
            cola_terminados.append(proceso)

            # pregunto por la cola de listos suspendidos
            if len(cola_listos_suspendidos) > 0:
                for proceso2 in cola_listos_suspendidos:
                    asignar_proceso_a_memoria(proceso2, cola_listos, cola_listos_suspendidos, suspendido=True)
                    break

        else:
            tiempo_general += QUANTO
            proceso['tiempo_irrupcion'] -= QUANTO
            # El proceso que se estaba ejecutando pasa al final de la cola de listos
            procesoEnEjecucion = cola_listos.pop(0)
            cola_listos.append(procesoEnEjecucion)
            
        agregarColaListos(procesos_ordenados, cola_listos, cola_listos_suspendidos, tiempo_general)
        
    imprimirTiempos(tiempos, tiempo_general, cantidad_procesos)


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
                asignar_proceso_a_memoria(proceso, cola_listos, cola_listos_suspendidos)
                    
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
    print('\nMemoria Principal:')
    headers = list(MEMORIA_PRINCIPAL[1].keys())
    header_line = f"| {'Partición':^10} | " + " | ".join([f"{h:^15}" for h in headers]) + " |"
    separator = '-' * len(header_line)

    print(separator)
    print(header_line)
    print(separator)

    for key, value in MEMORIA_PRINCIPAL.items():
        row = f"| {key:^10} | " + " | ".join([f"{str(v):^15}" for v in value.values()]) + " |"
        print(row)
        print(separator)


def imprimirTiempos(tiempos, tiempo_total, total_procesos):
    print('\n' + '=' * 60)
    print('Tiempo de retorno y espera de cada proceso:')
    print('-' * 60)

    # Encabezado de la tabla
    header = f"| {'Proceso':^10} | {'Tiempo Retorno':^15} | {'Tiempo Espera':^15} |"
    separator = '-' * len(header)

    print(header)
    print(separator)

    # Imprimir cada proceso con sus tiempos
    for tiempo in tiempos:
        proceso = tiempo['proceso']
        tiempo_retorno = tiempo['tiempo_retorno']
        tiempo_espera = tiempo['tiempo_espera']
        print(f"| {proceso:^10} | {tiempo_retorno:^15} | {tiempo_espera:^15} |")

    print(separator)

    # Cálculo y impresión de promedios
    tiempo_retorno_promedio = sum([t['tiempo_retorno'] for t in tiempos]) / len(tiempos)
    tiempo_espera_promedio = sum([t['tiempo_espera'] for t in tiempos]) / len(tiempos)

    print(f"| {'Promedio':^10} | {tiempo_retorno_promedio:^15.2f} | {tiempo_espera_promedio:^15.2f} |")
    print(separator)

    # Cálculo e impresión del rendimiento
    rendimiento = (total_procesos / tiempo_total) * 100
    print(f"Rendimiento: {rendimiento:.2f}%")
    print('=' * 60)



#######################################################
# Obteniedo datos de un archivo
# datos = obtener_datos('ejemplo3.csv')
datos = obtener_datos('ejemplo2.json')

# Ordenando datos segun tiempo de arribo
datos_ordenados = ordenar_datos(datos)

# Procesando cronograma
asignarMemoria(datos_ordenados)
import json
import time
import csv

# Constantes
QUANTO = 3


def round_robin(procesos, quanto=3):
    cronograma_falso = dict()
    cronograma = dict()
    no_times = 0
    time = 0

    while no_times < 10:
        for proceso in procesos:
            if (proceso["tiempo_arribo"] <= time) and (proceso['tiempo_irrupcion'] > 0):
                if proceso['tiempo_irrupcion'] - quanto <= 0:
                    time += proceso['tiempo_irrupcion']
                    proceso['tiempo_irrupcion'] = 0
                    no_times += 1
                else:
                    proceso["tiempo_irrupcion"] -= quanto
                    time += quanto

                cronograma_falso[time] = proceso["proceso_id"]
    
    # data = getData()
    for tiempo, nombre_proceso in cronograma_falso.items():
        for proceso in data:
            if (nombre_proceso==proceso['proceso_id']):
                cronograma[tiempo] = proceso

    return cronograma

def worst_fit(cola_listos, mp, finalizados):
    max_espacio_libre = 0
    max_indice = 0

    for key,value in mp.items():
        if value['espacio_ocupado']==0:
            espacio_libre = value['espacio_libre']-cola_listos[0]['tamanio']
            if espacio_libre > max_espacio_libre:
                max_espacio_libre = espacio_libre
                max_indice = key
    
    if max_indice != 0:
        mp[max_indice]['espacio_libre'] = max_espacio_libre
        mp[max_indice]['espacio_ocupado'] = cola_listos[0]['tamanio']
        finalizados.append(cola_listos[0])
        cola_listos.pop(0)
        # print(mp)
       # print(cola_listos)
        
    return [max_espacio_libre, max_indice]

def imprimir():
    pass

def calcular_tiempos():
    pass

def procesador(cronograma):
    cola_listos = cronograma[:5] # agrego primero cinco procesos
    cola_suspendidos = []
    finalizados = []
    mp = { 
       1: {
        'espacio_ocupado': 0,
        'espacio_libre': 250000
    }, 2: {
        'espacio_ocupado': 0,
        'espacio_libre': 150000
    }, 3: {
        'espacio_ocupado': 0,
        'espacio_libre': 50000
    }}
    fr_int = []
    fr_ext = []
    tiempo = cronograma[0].tiempo_arribo
    proceso_actual = cronograma[0].proceso_id

    
    while len(finalizados) != len(cronograma):

        while cola_listos['tiempo_arribo'] <= tiempo:
            cola_listos.append(cronograma[5+len(finalizados)])
            resultados = worst_fit(cola_listos, mp, finalizados)

            if resultados[1] == 0:
                break

        


        
        
        if proceso_actual != '':
            print(proceso_actual["proceso_id"], tiempo)
            finalizados.append(cronograma[len(finalizados)])
        else:
            tiempo += QUANTO

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

def cargar_datos(file_path):
    if file_path.endswith('.json'):
        return leer_json(file_path)
    elif file_path.endswith('.csv'):
        return leer_csv(file_path)
    else:
        raise ValueError("Formato de archivo no soportado. Usa JSON o CSV.")


#######################################################
data = cargar_datos('procesos.json')

cronograma = round_robin(data)

print(cronograma)
# procesador(cronograma)



from logica import obtener_datos, ordenar_datos, asignarMemoria


def mostrar_historial(historial):
    print('\nHistorial de la simulación:')
    for tiempo, cola_listos, cola_listos_suspendidos, cola_terminados, proceso, memoria_principal in historial:
        print('=' * 70)
        print(f'| {"Tiempo general":<20}: {tiempo:<45} |')
        print(f'| {"Proceso en ejecución":<20}: {proceso["proceso_id"]:<45} |')
        print(f'| {"Cola de listos":<20}: {", ".join([p["proceso_id"] for p in cola_listos]):<45} |')
        print(f'| {"Cola de listos suspendidos":<20}: {", ".join([p["proceso_id"] for p in cola_listos_suspendidos]):<39} |')
        print(f'| {"Cola de terminados":<20}: {", ".join([p["proceso_id"] for p in cola_terminados]):<45} |')
        print('=' * 70)

        # Encabezado de la tabla de memoria
        print(f'| {"Partición":^10} | {"Dir Inicial":^12} | {"Tamaño":^10} | {"Proceso":^10} | {"Estado":^10} | {"Frag. Interna":^14} |')
        print('-' * 85)

        # Mostrar las particiones de la memoria principal
        for key, value in memoria_principal.items():
            particion = f'| {key:^10} | {value["dir_inicial"]:^12} | {value["tamanio"]:^10} | {value["proceso"]:^10} | {value["estado"]:^10} | {value["fr_interna"]:^14} |'
            print(particion)
            print('-' * 85)

        input('Presiona Enter para continuar...')


def mostrar_tiempos(tiempos, tiempo_total, total_procesos):
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


if __name__ == "__main__":
    datos = obtener_datos('ejemplo1.json')
    datos_ordenados = ordenar_datos(datos)
    tiempos, historial, tiempo_final = asignarMemoria(datos_ordenados)

    mostrar_historial(historial)
    mostrar_tiempos(tiempos, tiempo_final, len(datos_ordenados))

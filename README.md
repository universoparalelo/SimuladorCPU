# Simulador de Procesador

Este proyecto es un **simulador de procesador** que implementa planificación de procesos usando **Round Robin** y asignación de memoria con **Worst Fit** utilizando particiones fijas. El simulador permite comprender conceptos fundamentales del manejo de procesos como las colas de **Listo** y **Listo Suspendido**.

## Tabla de contenidos

1. [Descripción](#descripción)
2. [Características](#características)
3. [Requisitos del sistema](#requisitos-del-sistema)
4. [Instalación](#instalación)
5. [Uso del programa](#uso-del-programa)
6. [Ejemplos](#ejemplos)
7. [Contribución](#contribución)

## Descripción

El simulador permite visualizar el funcionamiento de un procesador utilizando planificación **Round Robin**, una estrategia en la cual los procesos reciben una pequeña cantidad de tiempo de CPU de forma cíclica. La memoria se asigna utilizando el método de **Worst Fit**, donde las particiones de memoria son fijas y el proceso ocupa la partición más grande disponible.

El objetivo del proyecto es brindar una herramienta didáctica para estudiar la planificación de procesos y la gestión de memoria en sistemas operativos.

## Características

- **Planificación Round Robin**.
- **Asignación de memoria con Worst Fit** (particiones fijas).
- **Simulación de colas de Listo y Listo Suspendido**.
- **Interfaz gráfica y ejecución por consola**.
- **Ejecutables para facilidad de uso**.

## Requisitos del sistema

El simulador incluye un archivo ejecutable que funciona en cualquier sistema operativo (Windows, macOS, Linux). Si deseas ejecutar el código fuente, necesitarás:

- **Python 3.11.1**
- Librería **tkinter** (incluida por defecto en Python para la interfaz gráfica).

## Instalación

Para obtener el proyecto, clona este repositorio desde GitHub con el siguiente comando:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
```

La estructura del proyecto es la siguiente:

```
simulador-procesador/
├── ejecutable/
│   └── simulador.exe
├── codigo_fuente/
│   ├── consola.py
│   ├── ui.py
│   └── logica.py
└── ejemplos/
    ├── ejemplo1.json
    └── ejemplo2.json
```

## Uso del programa

### Ejecución del archivo ejecutable

1. Navega a la carpeta `ejecutable/`.
2. Ejecuta `simulador.exe` haciendo doble clic.
3. Para probar el simulador, ve a la carpeta `ejemplos/` y selecciona un archivo de ejemplo (por ejemplo, `ejemplo1.json`).

### Ejecución del código fuente

Si prefieres ejecutar el código fuente directamente, sigue estos pasos:

#### Opción 1: Modo consola

```bash
cd codigo_fuente
python consola.py
```

#### Opción 2: Interfaz gráfica

Asegúrate de tener instalada la librería `tkinter`. Luego, ejecuta:

```bash
cd codigo_fuente
python ui.py
```

## Ejemplos

En la carpeta `ejemplos/` encontrarás archivos JSON y CSV que puedes usar para probar el simulador. Los ejemplos muestran diferentes configuraciones de procesos y asignaciones de memoria.

## Contribución

Este proyecto es parte de un trabajo práctico para el curso de **Sistemas Operativos**. Si deseas contribuir, puedes crear un pull request o enviar tus sugerencias.

## Créditos

- **Curso**: Sistemas Operativos, Universidad UTN FRRe



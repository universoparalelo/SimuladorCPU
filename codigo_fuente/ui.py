import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from logica import obtener_datos, ordenar_datos, asignarMemoria

FUENTE = 'Helvetica'
COLOR_FONDO = '#1E1E2F'
COLOR_FUENTE = '#F8F8F2'
COLOR_BOTON_SIGUIENTE = '#1E88E5'

class SimuladorMemoria:
    def __init__(self):
        self.archivo_seleccionado = None
        self.instante = 0
        self.id_particion = 0
        self.cola_listos = []
        self.cola_suspendidos = []
        self.cola_terminados = []
        self.historial = []
        self.historial_index = 0

        # Crear la ventana de inicio
        self.ventana_inicio = tk.Tk()
        self.ventana_inicio.title("Simulador de Memoria")
        # Dimensiones deseadas
        self.ancho_ventana = 900
        self.alto_ventana = 650

        # Obtener el tamaño de la pantalla
        self.ancho_pantalla = self.ventana_inicio.winfo_screenwidth()
        self.alto_pantalla = self.ventana_inicio.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        self.posicion_x = (self.ancho_pantalla - self.ancho_ventana) // 2
        self.posicion_y = (self.alto_pantalla - self.alto_ventana) // 2

        # Establecer el tamaño y posición de la ventana
        self.ventana_inicio.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{self.posicion_x}+{self.posicion_y}")
        self.ventana_inicio.config(bg=COLOR_FONDO)

        # Etiqueta de bienvenida
        titulo_label = tk.Label(self.ventana_inicio, text="Simulador de Memoria", font=(FUENTE, 24), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        titulo_label.pack(pady=50)

        # Botón para seleccionar archivo
        boton_seleccionar_archivo = tk.Button(
            self.ventana_inicio, text="Seleccionar Archivo", font=(FUENTE, 18),
            command=self.seleccionar_archivo, 
            borderwidth=3,  # Grosor del borde
            relief="raised"
        )
        boton_seleccionar_archivo.pack(pady=10)

        # Botón para iniciar simulación
        self.boton_iniciar = tk.Button(
            self.ventana_inicio, text="Iniciar Simulación", font=(FUENTE, 18),
            command=self.mostrar_simulacion,
            borderwidth=3,  # Grosor del borde
            relief="raised"
        )
        self.boton_iniciar.pack(pady=10)

        # Ejecutar ventana de inicio
        self.ventana_inicio.mainloop()

    def seleccionar_archivo(self):
        # Abrir el diálogo para seleccionar un archivo .json o .csv
        self.archivo_seleccionado = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos JSON", "*.json"), ("Archivos CSV", "*.csv"))
        )
        if self.archivo_seleccionado:
            messagebox.showinfo("Archivo Seleccionado", f"Archivo seleccionado: {self.archivo_seleccionado}")
            self.boton_iniciar.config(bg=COLOR_BOTON_SIGUIENTE)

    def mostrar_simulacion(self):
        # Validar si se seleccionó un archivo antes de iniciar la simulación
        if not self.archivo_seleccionado:
            messagebox.showwarning("Archivo no seleccionado", "Debes seleccionar un archivo antes de iniciar la simulación.")
            return

        # Cerrar ventana de inicio y abrir la ventana de simulación
        self.ventana_inicio.destroy()

        # Leer los datos del archivo seleccionado
        datos = obtener_datos(self.archivo_seleccionado)
        datos_ordenados = ordenar_datos(datos)
        self.tiempos, self.historial, self.tiempo_final = asignarMemoria(datos_ordenados)

        # Crear ventana principal de simulación
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Memoria")
        self.ventana.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{self.posicion_x}+{self.posicion_y}")
        self.ventana.config(bg=COLOR_FONDO)

        # Etiquetas para instante e ID de partición
        self.instante_label = tk.Label(self.ventana, text=f"Instante = {self.instante}", font=(FUENTE, 18), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        self.instante_label.pack(pady=5)

        self.id_particion_label = tk.Label(self.ventana, text=f"Id_partición = {self.id_particion}", font=(FUENTE, 18), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        self.id_particion_label.pack(pady=5)

        # Etiquetas para colas
        self.cola_listos_label = tk.Label(self.ventana, text=f"Cola_listos = {', '.join(self.cola_listos)}", font=(FUENTE, 18), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        self.cola_listos_label.pack(pady=5)

        self.cola_suspendidos_label = tk.Label(self.ventana, text=f"Cola_listos_suspendidos = {', '.join(self.cola_suspendidos)}", font=(FUENTE, 18), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        self.cola_suspendidos_label.pack(pady=5)

        # Contenedor para la memoria principal
        memoria_frame = tk.Frame(self.ventana, width=350, height=400, bg=COLOR_FONDO)
        memoria_frame.pack(pady=15)

        # Particiones de memoria
        self.particion1_label = tk.Label(memoria_frame, text="id_partición = 1\n50kb\nFI (50kb)", font=(FUENTE, 16), bg="lightcoral", width=25, height=3)
        self.particion1_label.pack(pady=10)

        self.particion2_label = tk.Label(memoria_frame, text="id_partición = 2\n150kb\nFI (50kb)", font=(FUENTE, 16), bg="lightgreen", width=25, height=3)
        self.particion2_label.pack(pady=10)

        self.particion3_label = tk.Label(memoria_frame, text="id_partición = 3\n250kb\nFI (250kb)", font=(FUENTE, 16), bg="lightblue", width=25, height=3)
        self.particion3_label.pack(pady=10)

        # Cola de terminados
        self.cola_terminados_label = tk.Label(self.ventana, text=f"Cola_terminados = {', '.join(self.cola_terminados)}", font=(FUENTE, 18), bg=COLOR_FONDO, fg=COLOR_FUENTE)
        self.cola_terminados_label.pack(pady=5)

        # Botón de siguiente
        self.boton_siguiente = tk.Button(self.ventana, text="Siguiente", font=(FUENTE, 18), command=self.siguiente, bg=COLOR_BOTON_SIGUIENTE)
        self.boton_siguiente.pack(pady=10)

        # Actualizar las etiquetas con el primer estado del historial
        self.actualizar_etiquetas()

        # Ejecutar la ventana de simulación
        self.ventana.mainloop()

    def actualizar_etiquetas(self):
        # Obtener los datos del historial en el índice actual
        tiempo_general, cola_listos, cola_listos_suspendidos, cola_terminados, proceso, memoria_principal = self.historial[self.historial_index]

        # Actualizar las etiquetas con los datos del historial
        self.instante_label.config(text=f"Instante = {tiempo_general}")
        self.id_particion_label.config(text=f"Proceso en ejecucion = {proceso['proceso_id']}")
        self.cola_listos_label.config(text=f"Cola_listos = {', '.join([p['proceso_id'] for p in cola_listos])}")
        self.cola_suspendidos_label.config(text=f"Cola_listos_suspendidos = {', '.join([p['proceso_id'] for p in cola_listos_suspendidos])}")
        self.cola_terminados_label.config(text=f"Cola_terminados = {', '.join([p['proceso_id'] for p in cola_terminados])}")

        # Actualizar las particiones de memoria
        self.particion1_label.config(text=f"id_partición = 1\n{memoria_principal[1]['tamanio']}kb\n{memoria_principal[1]['proceso']} FI ({memoria_principal[1]['fr_interna']})")
        self.particion2_label.config(text=f"id_partición = 2\n{memoria_principal[2]['tamanio']}kb\n{memoria_principal[2]['proceso']} FI ({memoria_principal[2]['fr_interna']})")
        self.particion3_label.config(text=f"id_partición = 3\n{memoria_principal[3]['tamanio']}kb\n{memoria_principal[3]['proceso']} FI ({memoria_principal[3]['fr_interna']})")

    def siguiente(self):
        # Incrementar el índice del historial
        if self.historial_index < len(self.historial) - 1:
            self.historial_index += 1

            # Actualizar las etiquetas con los datos del historial
            self.actualizar_etiquetas()
            print(f"Avanzando al instante {self.historial[self.historial_index][0]}...")
        
        else:
            # Destruir la ventana actual y mostrar los tiempos
            self.ventana.destroy()
            self.mostrar_tiempos()

    def mostrar_tiempos(self):
        # Crear una nueva ventana para mostrar los tiempos
        ventana_tiempos = tk.Tk()
        ventana_tiempos.title("Tiempos de Procesos")
        ventana_tiempos.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{self.posicion_x}+{self.posicion_y}")

        ventana_tiempos.config(bg=COLOR_FONDO)

        # Crear un frame para la tabla
        frame_tabla = tk.Frame(ventana_tiempos, bg=COLOR_FONDO, borderwidth=1, relief="solid")
        frame_tabla.pack(pady=30, padx=10, expand=True)

        # Crear encabezados de la tabla
        encabezados = ["Proceso", "Tiempo de Retorno", "Tiempo de Espera"]
        for i, encabezado in enumerate(encabezados):
            label = tk.Label(frame_tabla, text=encabezado, font=(FUENTE, 15, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=20)
            label.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

        # Crear filas de la tabla con los tiempos de los procesos
        for i, tiempo in enumerate(self.tiempos):
            proceso_label = tk.Label(frame_tabla, text=tiempo['proceso'], font=(FUENTE, 15), fg=COLOR_FUENTE, bg=COLOR_FONDO, borderwidth=1, relief="solid", width=20)
            proceso_label.grid(row=i+1, column=0, padx=0, pady=0, sticky="nsew")
            retorno_label = tk.Label(frame_tabla, text=tiempo['tiempo_retorno'], font=(FUENTE, 15), fg=COLOR_FUENTE, bg=COLOR_FONDO, borderwidth=1, relief="solid", width=20)
            retorno_label.grid(row=i+1, column=1, padx=0, pady=0, sticky="nsew")
            espera_label = tk.Label(frame_tabla, text=tiempo['tiempo_espera'], font=(FUENTE, 15), fg=COLOR_FUENTE, bg=COLOR_FONDO, borderwidth=1, relief="solid", width=20)
            espera_label.grid(row=i+1, column=2, padx=0, pady=0, sticky="nsew")

        # Calcular y mostrar los promedios y rendimiento
        tiempo_retorno_promedio = sum([t['tiempo_retorno'] for t in self.tiempos]) / len(self.tiempos)
        tiempo_espera_promedio = sum([t['tiempo_espera'] for t in self.tiempos]) / len(self.tiempos)
        rendimiento = (len(self.tiempos) / self.tiempo_final) * 100

        # Mostrar los promedios en la última fila
        promedio_label = tk.Label(frame_tabla, text="Promedio", font=(FUENTE, 15, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=20)
        promedio_label.grid(row=len(self.tiempos) + 1, column=0, padx=0, pady=0, sticky="nsew")
        promedio_retorno_label = tk.Label(frame_tabla, text=f"{tiempo_retorno_promedio:.2f}", font=(FUENTE, 15), bg=COLOR_FONDO, fg=COLOR_FUENTE, borderwidth=1, relief="solid", width=20)
        promedio_retorno_label.grid(row=len(self.tiempos) + 1, column=1, padx=0, pady=0, sticky="nsew")
        promedio_espera_label = tk.Label(frame_tabla, text=f"{tiempo_espera_promedio:.2f}", font=(FUENTE, 15), fg=COLOR_FUENTE, bg=COLOR_FONDO, borderwidth=1, relief="solid", width=20)
        promedio_espera_label.grid(row=len(self.tiempos) + 1, column=2, padx=0, pady=0, sticky="nsew")

        # Mostrar el rendimiento en una fila adicional
        rendimiento_label = tk.Label(frame_tabla, text=f"Rendimiento: {rendimiento:.2f}%", font=(FUENTE, 15, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=60)
        rendimiento_label.grid(row=len(self.tiempos) + 2, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana_tiempos, text="Cerrar", font=(FUENTE, 18), bg=COLOR_BOTON_SIGUIENTE,           command=ventana_tiempos.destroy, borderwidth=3, relief="raised")
        boton_cerrar.pack(pady=70)

        # Ejecutar la ventana de tiempos
        ventana_tiempos.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    app = SimuladorMemoria()

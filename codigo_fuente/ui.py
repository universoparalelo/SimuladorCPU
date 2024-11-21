import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from logica import obtener_datos, ordenar_datos, asignarMemoria

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
        self.ventana_inicio.geometry("400x200")
        self.ventana_inicio.config(bg="white")

        # Etiqueta de bienvenida
        titulo_label = tk.Label(self.ventana_inicio, text="Simulador de Memoria", font=("Arial", 16), bg="white")
        titulo_label.pack(pady=10)

        # Botón para seleccionar archivo
        boton_seleccionar_archivo = tk.Button(
            self.ventana_inicio, text="Seleccionar Archivo", font=("Arial", 12),
            command=self.seleccionar_archivo
        )
        boton_seleccionar_archivo.pack(pady=10)

        # Botón para iniciar simulación
        boton_iniciar = tk.Button(
            self.ventana_inicio, text="Iniciar Simulación", font=("Arial", 12),
            command=self.mostrar_simulacion
        )
        boton_iniciar.pack(pady=10)

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
        self.ventana.geometry("500x500")
        self.ventana.config(bg="white")

        # Etiquetas para instante e ID de partición
        self.instante_label = tk.Label(self.ventana, text=f"Instante = {self.instante}", font=("Arial", 12), bg="white")
        self.instante_label.pack(pady=5)

        self.id_particion_label = tk.Label(self.ventana, text=f"Id_partición = {self.id_particion}", font=("Arial", 12), bg="white")
        self.id_particion_label.pack(pady=5)

        # Etiquetas para colas
        self.cola_listos_label = tk.Label(self.ventana, text=f"Cola_listos = {', '.join(self.cola_listos)}", font=("Arial", 12), bg="white")
        self.cola_listos_label.pack(pady=5)

        self.cola_suspendidos_label = tk.Label(self.ventana, text=f"Cola_listos_suspendidos = {', '.join(self.cola_suspendidos)}", font=("Arial", 12), bg="white")
        self.cola_suspendidos_label.pack(pady=5)

        # Contenedor para la memoria principal
        memoria_frame = tk.Frame(self.ventana, width=300, height=400, bg="lightgray", relief="solid", borderwidth=2)
        memoria_frame.pack(pady=10)

        # Particiones de memoria
        self.particion1_label = tk.Label(memoria_frame, text="id_partición = 1\n50kb\nFI (50kb)", font=("Arial", 10), bg="lightcoral", width=25, height=3, relief="solid")
        self.particion1_label.pack(pady=5)

        self.particion2_label = tk.Label(memoria_frame, text="id_partición = 2\n150kb\nFI (50kb)", font=("Arial", 10), bg="lightgreen", width=25, height=3, relief="solid")
        self.particion2_label.pack(pady=5)

        self.particion3_label = tk.Label(memoria_frame, text="id_partición = 3\n250kb\nFI (250kb)", font=("Arial", 10), bg="lightblue", width=25, height=3, relief="solid")
        self.particion3_label.pack(pady=5)

        # Cola de terminados
        self.cola_terminados_label = tk.Label(self.ventana, text=f"Cola_terminados = {', '.join(self.cola_terminados)}", font=("Arial", 12), bg="white")
        self.cola_terminados_label.pack(pady=5)

        # Botón de siguiente
        self.boton_siguiente = tk.Button(self.ventana, text="Siguiente", font=("Arial", 12), command=self.siguiente)
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
        ventana_tiempos.geometry("700x500")
        ventana_tiempos.config(bg="white")

        # Crear un frame para la tabla
        frame_tabla = tk.Frame(ventana_tiempos, bg="white")
        frame_tabla.pack(pady=20)

        # Crear encabezados de la tabla
        encabezados = ["Proceso", "Tiempo de Retorno", "Tiempo de Espera"]
        for i, encabezado in enumerate(encabezados):
            label = tk.Label(frame_tabla, text=encabezado, font=("Arial", 12, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=20)
            label.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

        # Crear filas de la tabla con los tiempos de los procesos
        for i, tiempo in enumerate(self.tiempos):
            proceso_label = tk.Label(frame_tabla, text=tiempo['proceso'], font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=20)
            proceso_label.grid(row=i+1, column=0, padx=0, pady=0, sticky="nsew")
            retorno_label = tk.Label(frame_tabla, text=tiempo['tiempo_retorno'], font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=20)
            retorno_label.grid(row=i+1, column=1, padx=0, pady=0, sticky="nsew")
            espera_label = tk.Label(frame_tabla, text=tiempo['tiempo_espera'], font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=20)
            espera_label.grid(row=i+1, column=2, padx=0, pady=0, sticky="nsew")

        # Calcular y mostrar los promedios y rendimiento
        tiempo_retorno_promedio = sum([t['tiempo_retorno'] for t in self.tiempos]) / len(self.tiempos)
        tiempo_espera_promedio = sum([t['tiempo_espera'] for t in self.tiempos]) / len(self.tiempos)
        rendimiento = (len(self.tiempos) / self.tiempo_final) * 100

        # Mostrar los promedios en la última fila
        promedio_label = tk.Label(frame_tabla, text="Promedio", font=("Arial", 12, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=20)
        promedio_label.grid(row=len(self.tiempos) + 1, column=0, padx=0, pady=0, sticky="nsew")
        promedio_retorno_label = tk.Label(frame_tabla, text=f"{tiempo_retorno_promedio:.2f}", font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=20)
        promedio_retorno_label.grid(row=len(self.tiempos) + 1, column=1, padx=0, pady=0, sticky="nsew")
        promedio_espera_label = tk.Label(frame_tabla, text=f"{tiempo_espera_promedio:.2f}", font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=20)
        promedio_espera_label.grid(row=len(self.tiempos) + 1, column=2, padx=0, pady=0, sticky="nsew")

        # Mostrar el rendimiento en una fila adicional
        rendimiento_label = tk.Label(frame_tabla, text=f"Rendimiento: {rendimiento:.2f}%", font=("Arial", 12, "bold"), bg="lightblue", borderwidth=1, relief="solid", width=60)
        rendimiento_label.grid(row=len(self.tiempos) + 2, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana_tiempos, text="Cerrar", font=("Arial", 12), command=ventana_tiempos.destroy)
        boton_cerrar.pack(pady=10)

        # Ejecutar la ventana de tiempos
        ventana_tiempos.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    app = SimuladorMemoria()

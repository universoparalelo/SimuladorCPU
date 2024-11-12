import tkinter as tk

# Función para avanzar al siguiente instante
def siguiente():
    print("Avanzando al siguiente instante...")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Simulación de Memoria")
ventana.geometry("500x600")
ventana.config(bg="white")

# Instante de tiempo y ID de partición
instante_label = tk.Label(ventana, text="Instante = 0", font=("Arial", 12), bg="white")
instante_label.pack(pady=5)

id_particion_label = tk.Label(ventana, text="Id_partición = 2", font=("Arial", 12), bg="white")
id_particion_label.pack(pady=5)

# Cola de listos
cola_listos_label = tk.Label(ventana, text="Cola_listos = P3, P4", font=("Arial", 12), bg="white")
cola_listos_label.pack(pady=5)

# Cola de listos suspendidos
cola_suspendidos_label = tk.Label(ventana, text="Cola_listos_suspendidos = P6, P7", font=("Arial", 12), bg="white")
cola_suspendidos_label.pack(pady=5)

# Contenedor para la memoria principal
memoria_frame = tk.Frame(ventana, width=300, height=400, bg="lightgray", relief="solid", borderwidth=2)
memoria_frame.pack(pady=10)

# Partición 1
particion1_label = tk.Label(memoria_frame, text="id_partición = 1\n150kb\nFI (50kb)", font=("Arial", 10), bg="lightcoral", width=25, height=3, relief="solid")
particion1_label.pack(pady=5)

# Partición 2
particion2_label = tk.Label(memoria_frame, text="id_partición = 2\n200kb\nP2 (50kb)", font=("Arial", 10), bg="lightgreen", width=25, height=3, relief="solid")
particion2_label.pack(pady=5)

# Partición 3
particion3_label = tk.Label(memoria_frame, text="id_partición = 3\n250kb\nP5 (250kb)", font=("Arial", 10), bg="lightblue", width=25, height=3, relief="solid")
particion3_label.pack(pady=5)

# Cola de terminados
cola_terminados_label = tk.Label(ventana, text="Cola_terminados = P6, P7", font=("Arial", 12), bg="white")
cola_terminados_label.pack(pady=5)

# Botón de siguiente
boton_siguiente = tk.Button(ventana, text="Siguiente", font=("Arial", 12), command=siguiente)
boton_siguiente.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()

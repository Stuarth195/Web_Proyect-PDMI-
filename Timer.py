import tkinter as tk


class TimerApp:
    def __init__(self, root):
        self.root = root

        self.time_left = 10  # Temporizador en segundos

        # Etiqueta para mostrar el tiempo
        self.label = tk.Label(self.root, text=f"Tiempo restante hasta la entrega: {self.time_left}m", font=("Helvetica", 10, "bold"), bg="white")
        self.label.place(x=1100, y=8)

    def start_timer(self, time):
        self.time_left = time  # Resetear el temporizador a 10 segundos
        self.update_timer()  # Comenzar a actualizar el temporizador visual

    def update_timer(self):
        # Actualizar el texto de la etiqueta con el tiempo restante
        self.label.config(text=f"Tiempo restante hasta la entrega: {self.time_left}m")

        if self.time_left > 0:
            self.time_left -= 1
            # Llamar a esta función nuevamente después de 1000 ms (1 segundo)
            self.root.after(60000, self.update_timer)

    def extra_action(self):
        print("Se ejecutó la acción extra.")


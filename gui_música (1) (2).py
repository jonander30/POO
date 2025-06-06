# -*- coding: utf-8 -*-
"""GUI_música.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18dDkQM0yp6n8TnJsyuhtZosHxgKObNyq
"""

import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Música")

        # Inicializar pygame
        pygame.init()
        pygame.mixer.init()

        # Variables
        self.playlist = []
        self.current_index = 0
        self.paused = False
        self.volume = 0.7

        # GUI
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)

        # Lista de reproducción
        self.playlist_box = tk.Listbox(main_frame, width=50, height=15, selectmode=tk.SINGLE)
        self.playlist_box.grid(row=0, column=0, columnspan=5, pady=10)

        # Botones
        btn_add = tk.Button(main_frame, text="Añadir", command=self.add_songs)
        btn_add.grid(row=1, column=0, padx=5)

        btn_remove = tk.Button(main_frame, text="Quitar", command=self.remove_song)
        btn_remove.grid(row=1, column=1, padx=5)

        btn_play = tk.Button(main_frame, text="Reproducir", command=self.play_song)
        btn_play.grid(row=1, column=2, padx=5)

        btn_pause = tk.Button(main_frame, text="Pausa", command=self.pause_song)
        btn_pause.grid(row=1, column=3, padx=5)

        btn_stop = tk.Button(main_frame, text="Detener", command=self.stop_song)
        btn_stop.grid(row=1, column=4, padx=5)

        # Barra de volumen
        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=10)

        tk.Label(volume_frame, text="Volumen:").pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.set_volume)
        self.volume_slider.set(self.volume * 100)
        self.volume_slider.pack(side=tk.LEFT)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10)

        # Etiqueta de tiempo
        self.time_label = tk.Label(self.root, text="00:00 / 00:00")
        self.time_label.pack()

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")])
        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))

    def remove_song(self):
        selected = self.playlist_box.curselection()
        if selected:
            index = selected[0]
            self.playlist_box.delete(index)
            self.playlist.pop(index)

    def play_song(self):
        if not pygame.mixer.music.get_busy() and self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.update_progress()

    def pause_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_song(self):
        pygame.mixer.music.stop()

    def set_volume(self, val):
        self.volume = float(val) / 100
        pygame.mixer.music.set_volume(self.volume)

    def update_progress(self):
        # Esta función necesitaría ser más elaborada para mostrar el progreso real
        current_time = pygame.mixer.music.get_pos() / 1000
        # Aquí deberías obtener la duración total de la canción (requiere biblioteca adicional)
        total_time = 180  # Ejemplo: 3 minutos

        if current_time < total_time:
            self.progress['value'] = (current_time / total_time) * 100
            mins, secs = divmod(int(current_time), 60)
            total_mins, total_secs = divmod(int(total_time), 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d} / {total_mins:02d}:{total_secs:02d}")
            self.root.after(1000, self.update_progress)

def create_new_player():
    new_window = tk.Toplevel()
    MusicPlayer(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)

    # Botón para crear nueva instancia
    new_player_btn = tk.Button(root, text="Nuevo Reproductor", command=create_new_player)
    new_player_btn.pack(pady=10)

    root.mainloop()
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import time
import threading

# Initialize pygame mixer
pygame.mixer.init()

class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music App")
        self.root.geometry("500x300")

        # Playlist
        self.playlist = []
        self.current_index = 0
        self.is_playing = False

        # UI Elements
        self.playlist_box = tk.Listbox(root, width=50)
        self.playlist_box.pack(pady=10)

        controls_frame = tk.Frame(root)
        controls_frame.pack()

        self.load_button = tk.Button(controls_frame, text="Load", command=self.load_song)
        self.load_button.grid(row=0, column=0, padx=5)

        self.play_button = tk.Button(controls_frame, text="Play", command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=5)

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=5)

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=5)

        self.next_button = tk.Button(controls_frame, text="Next", command=self.next_song)
        self.next_button.grid(row=0, column=4, padx=5)

        self.prev_button = tk.Button(controls_frame, text="Prev", command=self.prev_song)
        self.prev_button.grid(row=0, column=5, padx=5)

        # Volume control
        self.volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.1,
                                      orient="horizontal", label="Volume",
                                      command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

    def load_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.playlist.append(file_path)
            self.playlist_box.insert(tk.END, file_path.split("/")[-1])

    def play_song(self):
        if self.playlist:
            song = self.playlist[self.current_index]
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.is_playing = True
            threading.Thread(target=self.update_progress, daemon=True).start()

    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def update_progress(self):
        while self.is_playing:
            try:
                # pygame doesn't give duration directly, so we simulate
                self.progress['value'] += 1
                if self.progress['value'] >= 100:
                    self.progress['value'] = 0
                time.sleep(1)
            except:
                break

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
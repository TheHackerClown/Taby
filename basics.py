import tkinter as tk
import pygame

def play_music():
    pygame.mixer.music.play()
global paused
paused = False
def pause_music():
    if paused == False:
        pygame.mixer.music.pause()
        paused = True
    elif paused:
        pygame.mixer.music.unpause()
        paused = False

def stop_music():
    pygame.mixer.music.stop()

window = tk.Tk()
window.title("Music Player")
window.geometry("500x300")

play_button = tk.Button(window, text="Play", command=play_music)
pause_button = tk.Button(window, text="Pause", command=pause_music)
stop_button = tk.Button(window, text="Stop", command=stop_music)

pygame.init()
pygame.mixer.init()
music_file = "Assassination.wav"
pygame.mixer.music.load(music_file)

play_button.pack()
pause_button.pack()
stop_button.pack()

window.mainloop()

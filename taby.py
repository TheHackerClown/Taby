import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,ttk,Listbox,Frame,filedialog,END,messagebox
from sv_ttk import set_theme
from pygame import mixer
from mutagen.mp3 import MP3
import time
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / 'assets'
mixer.init()

def getfile(path: str) -> Path:
        return ASSETS_PATH / Path(path)

master = Tk()

icon = PhotoImage(file=getfile(path='music.png'))
master.iconphoto(True, icon)
master.title('Taby - Music Player')
master.geometry('600x300')
master.configure(bg='#FFFFFF')

interval_function = False
settings,pause,user_input = {'RATE':0},True,True

#Functions
def get_mp3_duration(file_path):
    audio = MP3(file_path)
    duration_in_seconds = audio.info.length
    return duration_in_seconds


#VOLUME INCREASE OR DECREASE {PERFECTLY WORKING DONT TOUCH}
def vol_slider_change(value):
        volume = float(value) / 100
        mixer.music.set_volume(volume)

def increase(value):
        global user_input
        if user_input and mixer.music.get_busy():
                mixer.music.set_pos(float(value))
                canvas.itemconfigure(song_lenth_canvas, text=f"{return_time(value)}/{return_time(main_scale['to'])}")
        else:
                canvas.itemconfigure(song_lenth_canvas, text=f"{return_time(value)}/{return_time(main_scale['to'])}")

#DELETE SONG {PERFECTLY WORKING DONT TOUCH}
def delete_song(obj):
        selected_index = obj.curselection()[0]
        song = obj.get(selected_index) +'.mp3'
        obj.delete(selected_index)
        path = settings["DIR"] / song
        os.remove(path)
        
#ADDING SONGS FROM A DIRECTORY {PERFECTLY WORKING DONT TOUCH}
def add_song(obj):
        global settings
        directory = filedialog.askdirectory()
        if directory:
                settings["DIR"] = directory
                obj.delete(0,END)
                mp3_files = [file for file in os.listdir(directory) if file.endswith(".mp3")]
                for mp3_file in enumerate(mp3_files):
                        obj.insert(mp3_file[0], mp3_file[1][:-4])

def reset_player():
       global pause
       global user_input
       pause=True
       user_input = False
       main_scale.set(0)
       user_input = True
       main_scale['to'] = 100
       mixer.music.unload()
       canvas.itemconfigure(song_lenth_canvas, text="00:00/00:00")
       canvas.itemconfigure(song_name_canvas,text='Select A Song')
       song_list.selection_clear(0, END)

def return_time(value):
       value = int(round(float(value)))
       if value >= 60 and value//60 <10 and value%60>9:
              return f'0{value//60}:{value%60}'
       elif value == 0:
              return f"00:00"
       elif value < 60 and value >9:
              return f"00:{value}"
       elif value <=9 and value >0:
              return f"00:0{value}"
       elif value > 60 and value//60 >=10 and value%60>9:
              return f'{value//60}:{value%60}'
       elif value > 60 and value//60 >=10 and value%60<=9:
              return f'{value//60}:0{value%60}'
       elif value >= 60 and value//60 <10 and value%60<=9:
              return f"0{value//60}:0{value%60}"
       

def play(obj):
        global pause
        global interval_function
        global user_input
        index = obj.curselection()
        if index and settings['DIR']:
                if interval_function:
                       main_scale.after_cancel(interval_function)
                global pause
                pause = False
                song_name = obj.get(obj.curselection())
                song_path = settings['DIR'] +'/'+ song_name + '.mp3'
                canvas.itemconfigure(song_name_canvas,text=song_name)
                mixer.music.load(str(song_path))
                main_scale['to'] = round(get_mp3_duration(song_path))
                mixer.music.play()
                user_input= False
                main_scale.set(0)
                canvas.itemconfigure(song_lenth_canvas, text="00:00/00:00")
                user_input=True
                main_scale.after(100,increment_value(main_scale))

def next(obj):
        global pause
        global interval_function
        pause = False
        index = obj.curselection()[0]
        main_scale.after_cancel(interval_function)
        if index and index != obj.size()-1:
              obj.selection_clear(0,END)
              obj.selection_set(index+1)
              play(obj)
        elif index:
                obj.selection_clear(0,END)
                obj.selection_set(0)
                play(obj)

def prev(obj):
        global pause
        pause = False
        index = obj.curselection()[0]
        main_scale.after_cancel(interval_function)
        if index and index != 0:
              obj.selection_clear(0,END)
              obj.selection_set(index-1)
              play(obj)
        elif index:
                obj.selection_clear(0,END)
                obj.selection_set(obj.size() - 1)
                play(obj)
                

def increment_value(scale, interval=1000, increment_amount=1):
    global user_input,interval_function
    current_value = scale.get()
    new_value = current_value + increment_amount
    if new_value < scale['to'] and not pause:
        user_input = False
        scale.set(new_value)
        user_input = True
        interval_function = scale.after(interval, lambda: increment_value(scale, interval, increment_amount))
    elif new_value == scale['to']:
           user_input = False
           scale.set(scale['to'])
           user_input = True
           time.sleep(1.0)
    elif new_value > scale['to']:
           reset_player()
    else:    
           pass


def play_or_pause():
        global pause
        global interval_function
        if pause:
                pause=False
                mixer.music.unpause()
                main_scale.after(100,increment_value(main_scale))
        else:
                pause = True
                mixer.music.pause()

canvas = Canvas(
            master,
            bg = "#FFFFFF",
            height = 300,
            width = 600,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
canvas.place(x = 0, y = 0) 
bg_file = PhotoImage(
file=getfile(path="bg.png"))
background_image = canvas.create_image(
            300.0,
            150.0,
            image=bg_file
        )

prev_image = PhotoImage(
            file=getfile(path="prev.png"))
previous = Button(
            image=prev_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: prev(song_list),
            relief="flat"
        )
previous.place(
            x=316.0,
            y=72.0,
            width=30.000000000000004,
            height=30.0
        )

next_image = PhotoImage(
            file=getfile(path="next.png"))
next_btn = Button(
            image=next_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: next(song_list),
            relief="flat"
        )
next_btn.place(
            x=422.0,
            y=72.0,
            width=30.0,
            height=30.0
        )

play_pause_image = PhotoImage(
            file=getfile(path="play_pause.png"))
play_pause = Button(
            image=play_pause_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: play_or_pause(),
            relief="flat"
        )
play_pause.place(
            x=364.0,
            y=72.0,
            width=40.0,
            height=40.0
        )

help_image = PhotoImage(
            file=getfile(path="help.png"))
help_btn = Button(
            image=help_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: messagebox.showinfo('HELP!!!', 'Dhruv bhai se puchle abhi ke liye.\nVersion 2 mein aayega help function'),
            relief="flat"
        )
help_btn.place(
            x=4.0,
            y=252.0,
            width=34.0,
            height=43.0
        )

home_image = PhotoImage(
            file=getfile(path="home.png"))
home = Button(
            image=home_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
home.place(
            x=4.0,
            y=6.0,
            width=34.0,
            height=43.0
        )

cd_image = PhotoImage(
            file=getfile(path="cd_image.png"))
cd_image_on_canvas = canvas.create_image(
            126.0,
            61.0,
            image=cd_image
        )

open_file_image = PhotoImage(
            file=getfile(path="open_file.png"))
open_file = Button(
            image=open_file_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_song(song_list),
            relief="flat"
        )
open_file.place(
            x=85.0,
            y=239.0,
            width=82.0,
            height=33.0
        )

listbox_frame = Frame(master)
listbox_frame.place(x=209,y=124)

song_list = Listbox(listbox_frame, height=10,width=55)
scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=song_list.yview)

song_list.configure(yscrollcommand=scrollbar.set)
song_list.pack(side='left')
scrollbar.pack(side="right",fill='y')

song_list.insert(0, 'Click Open File Button, and select your music folder')


delete_image = PhotoImage(
            file=getfile(path="delete.png"))
delete_btn = Button(
            image=delete_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_song(song_list),
            relief="flat"
        )
delete_btn.place(
            x=85.0,
            y=199.0,
            width=82.0,
            height=33.0
        )

start_image = PhotoImage(
            file=getfile(path="start_song.png"))
start = Button(
            image=start_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: play(song_list),
            relief="flat"
        )
start.place(
            x=85.0,
            y=160.0,
            width=82.0,
            height=33.0
        )

main_scale = ttk.Scale(orient='horizontal',length=325,from_=0, command=lambda x: increase(x))
main_scale.place(x=219,y=35)

vol_scale = ttk.Scale(orient='horizontal',length=70,from_=0,to=100, command=vol_slider_change)
vol_scale.place(x=475,y=60)
vol_scale.set(100)
mixer.music.set_volume(1)

song_name_canvas = canvas.create_text(
            239.0,
            19.0,
            anchor="nw",
            text="Select A Song",
            fill="#FFFFFF",
            font=("Inter", 12 * -1)
        )
song_lenth_canvas = canvas.create_text(
            232.0,
            65.0,
            anchor="nw",
            text="00:00/00:00",
            fill="#FFFFFF",
            font=("Inter", 12 * -1)
        )

master.resizable(False, False)
set_theme('dark')
master.mainloop()

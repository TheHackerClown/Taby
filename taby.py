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


class Taby(Tk):
        def __init__(self, *args, **kwargs):
                super().__init__()
                self.wm_title("Taby - Music Player")
                self.geometry('600x300')
                self.configure(bg="#FFFFFF")
                self.icon = PhotoImage(file=self.getfile(path='music.png'))
                self.iconphoto(True, self.icon)
                self.interval_function = False
                self.settings = {'RATE':0}
                self.pause = True
                self.user_input = True
                self.resizable(False,False)
                self.canvas = Canvas(
                        self,
                        bg = "#FFFFFF",
                        height = 300,
                        width = 600,
                        bd = 0,
                        highlightthickness = 0,
                        relief = "ridge"
                        )
                self.canvas.place(x = 0, y = 0) 

                self.draw_elements()

        def getfile(self, path:str)->Path:
               return ASSETS_PATH / Path(path)

        #Functions
        def get_mp3_duration(self,file_path):
                audio = MP3(file_path)
                duration_in_seconds = audio.info.length
                return duration_in_seconds

        #VOLUME INCREASE OR DECREASE
        def vol_slider_change(self,value):
                volume = float(value) / 100
                mixer.music.set_volume(volume)


        def increase(self,value):
                if self.user_input and mixer.music.get_busy():
                        mixer.music.set_pos(float(value))
                        self.canvas.itemconfigure(self.song_lenth_canvas, text=f"{self.return_time(value)}/{self.return_time(self.main_scale['to'])}")
                else:
                        self.canvas.itemconfigure(self.song_lenth_canvas, text=f"{self.return_time(value)}/{self.return_time(self.main_scale['to'])}")

        #DELETE SONG
        def delete_song(self,obj):
                selected_index = obj.curselection()[0]
                song = obj.get(selected_index) +'.mp3'
                obj.delete(selected_index)
                path = self.settings["DIR"] / song
                os.remove(path)
                
        #ADDING SONGS FROM A DIRECTORY
        def add_song(self,obj):
                directory = filedialog.askdirectory()
                if directory:
                        self.settings["DIR"] = directory
                        obj.delete(0,END)
                        mp3_files = [file for file in os.listdir(directory) if file.endswith(".mp3")]
                        for mp3_file in enumerate(mp3_files):
                                obj.insert(mp3_file[0], mp3_file[1][:-4])

        def reset_player(self):
                self.pause=True
                self.user_input = False
                self.main_scale.set(0)
                self.user_input = True
                self.main_scale['to'] = 100
                mixer.music.unload()
                self.canvas.itemconfigure(self.song_lenth_canvas, text="00:00/00:00")
                self.canvas.itemconfigure(self.song_name_canvas,text='Select A Song')
                self.song_list.selection_clear(0, END)

        def return_time(self,value):
                value = int(round(float(value)))
                return f"{str(value//60).zfill(2)}:{str(value%60).zfill(2)}"
        
        def play(self,obj):
                index = obj.curselection()
                if index and self.settings['DIR']:
                        if self.interval_function:
                                self.main_scale.after_cancel(self.interval_function) 
                        self.pause = False
                        song_name = obj.get(obj.curselection())
                        song_path = self.settings['DIR'] +'/'+ song_name + '.mp3'
                        self.canvas.itemconfigure(self.song_name_canvas,text=song_name)
                        mixer.music.load(str(song_path))
                        self.main_scale['to'] = round(self.get_mp3_duration(song_path))
                        mixer.music.play()
                        self.user_input= False
                        self.main_scale.set(0)
                        self.canvas.itemconfigure(self.song_lenth_canvas, text="00:00/00:00")
                        self.user_input=True
                        self.main_scale.after(100,self.increment_value(self.main_scale))

        def next(self,obj):
                self.pause = False
                index = obj.curselection()[0]
                self.main_scale.after_cancel(self.interval_function)
                obj.selection_clear(0,END)
                obj.selection_set( index+1 if index and index != obj.size()-1 else 0 )
                self.play(obj)

        def prev(self,obj):
                self.pause = False
                index = obj.curselection()[0]
                self.main_scale.after_cancel(self.interval_function)
                obj.selection_clear(0,END)
                obj.selection_set(index-1 if index and index != 0 else obj.size() - 1)
                self.play(obj)

        def increment_value(self,scale, interval=1000, increment_amount=1):
                current_value = scale.get()
                new_value = current_value + increment_amount
                if new_value < scale['to'] and not self.pause:
                        self.user_input = False
                        scale.set(new_value)
                        self.user_input = True
                        self.interval_function = scale.after(interval, lambda: self.increment_value(scale, interval, increment_amount))
                elif new_value == scale['to']:
                        self.user_input = False
                        scale.set(scale['to'])
                        self.user_input = True
                        time.sleep(1.0)
                elif new_value > scale['to']:
                        self.reset_player()
                else:    
                        pass


        def play_or_pause(self):
                if self.pause:
                        self.pause=False
                        mixer.music.unpause()
                        self.main_scale.after(100,self.increment_value(self.main_scale))
                else:
                        self.pause = True
                        mixer.music.pause()

        def draw_elements(self):
               

               #Keep a reference of all PhotoImage to self instance, as else it will be removed by garbage collector
                self.bg_file = PhotoImage(
                file=self.getfile(path="bg.png"))
                
                self.canvas.create_image(
                        300.0,
                        150.0,
                        image=self.bg_file
                        )

                self.prev_image = PhotoImage(
                        file=self.getfile(path="prev.png"))
                previous = Button(
                        image=self.prev_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.prev(self.song_list),
                        relief="flat"
                        )
                previous.place(
                        x=316.0,
                        y=72.0,
                        width=30.000000000000004,
                        height=30.0
                        )

                self.next_image = PhotoImage(
                        file=self.getfile(path="next.png"))
                next_btn = Button(
                        image=self.next_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.next(self.song_list),
                        relief="flat"
                        )
                next_btn.place(
                        x=422.0,
                        y=72.0,
                        width=30.0,
                        height=30.0
                        )

                self.play_pause_image = PhotoImage(
                        file=self.getfile(path="play_pause.png"))
                play_pause = Button(
                        image=self.play_pause_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.play_or_pause(),
                        relief="flat"
                        )
                play_pause.place(
                        x=364.0,
                        y=72.0,
                        width=40.0,
                        height=40.0
                        )

                self.help_image = PhotoImage(
                        file=self.getfile(path="help.png"))
                help_btn = Button(
                        image=self.help_image,
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

                self.home_image = PhotoImage(
                        file=self.getfile(path="home.png"))
                
                home = Button(
                        image=self.home_image,
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

                self.cd_image = PhotoImage(
                        file=self.getfile(path="cd_image.png"))
                
                self.canvas.create_image(
                        126.0,
                        61.0,
                        image=self.cd_image
                        )

                self.open_file_image = PhotoImage(
                        file=self.getfile(path="open_file.png"))
                open_file = Button(
                        image=self.open_file_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.add_song(self.song_list),
                        relief="flat"
                        )
                open_file.place(
                        x=85.0,
                        y=239.0,
                        width=82.0,
                        height=33.0
                        )

                self.listbox_frame = Frame(self)
                self.listbox_frame.place(x=209,y=124)

                self.song_list = Listbox(self.listbox_frame, height=10,width=55)
                self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.song_list.yview)

                self.song_list.configure(yscrollcommand=self.scrollbar.set)
                self.song_list.pack(side='left')
                self.scrollbar.pack(side="right",fill='y')

                self.song_list.insert(0, 'Click Open File Button, and select your music folder')

                self.delete_image = PhotoImage(
                        file=self.getfile(path="delete.png"))
                delete_btn = Button(
                        image=self.delete_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.delete_song(self.song_list),
                        relief="flat"
                        )
                delete_btn.place(
                        x=85.0,
                        y=199.0,
                        width=82.0,
                        height=33.0
                        )

                self.start_image = PhotoImage(
                        file=self.getfile(path="start_song.png"))
                start = Button(
                        image=self.start_image,
                        borderwidth=0,
                        highlightthickness=0,
                        command=lambda: self.play(self.song_list),
                        relief="flat"
                        )
                start.place(
                        x=85.0,
                        y=160.0,
                        width=82.0,
                        height=33.0
                        )

                self.main_scale = ttk.Scale(orient='horizontal',length=325,from_=0, command=lambda x: self.increase(x))
                self.main_scale.place(x=219,y=35)

                vol_scale = ttk.Scale(orient='horizontal',length=70,from_=0,to=100, command=self.vol_slider_change)
                vol_scale.place(x=475,y=60)
                vol_scale.set(100)
                mixer.music.set_volume(1)

                self.song_name_canvas = self.canvas.create_text(
                        239.0,
                        19.0,
                        anchor="nw",
                        text="Select A Song",
                        fill="#FFFFFF",
                        font=("Inter", 12 * -1)
                        )
                self.song_lenth_canvas = self.canvas.create_text(
                        232.0,
                        65.0,
                        anchor="nw",
                        text="00:00/00:00",
                        fill="#FFFFFF",
                        font=("Inter", 12 * -1)
                        )

if __name__ == "__main__":
        master = Taby()
        set_theme("dark")
        master.mainloop()

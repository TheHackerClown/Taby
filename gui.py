from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,Listbox, END,HORIZONTAL,Toplevel,messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import Style,Scale
from os import remove,listdir
from pygame import mixer,get_error,error
from pycaw.pycaw import AudioUtilities
from customtkinter import CTkSlider,CTkScrollbar
import webbrowser
import time
import audioread

#completely relate all image files to asset folder
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('assets/')
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

mixer.init()


#variable definition
playing_song,directory,paused,audio_files,sessions,opened,audio_folder,music_len = 0,'',False,[],AudioUtilities.GetAllSessions(),0,'assets/music/',1


#functions as it needs to be defined

def duration_finder(path):
    a = audioread.audio_open(path=path)
    total = a.duration
    return int(total)

def play_slider():
    a = main_slider.get()
    if paused == False:
        b = mixer.music.get_pos()
        main_slider.set(b)
        play_slider()
    elif paused == True:
        time.sleep(1)




def play_music():
    global paused
    global playing_song
    if playing_song==0:
        index = song_list.curselection()
        if index:
            selected_item = song_list.get(index)
            canvas.itemconfigure(Song_name,text=(selected_item))
        mixer.music.load("/".join([all_path if opened!=0 else audio_folder, str(selected_item)]))
        playing_song+=1
        #music_len = duration_finder("/".join([all_path if opened!=0 else audio_folder, str(selected_item)]))
        main_slider.configure(to=100)
        mixer.music.play()
        play_slider()
    elif playing_song !=0:
        paused=True
        mixer.music.unload()
        index = song_list.curselection()
        if index:
            selected_item = song_list.get(index)
            canvas.itemconfigure(Song_name,text=(selected_item))
        mixer.music.unload()
        try:
            mixer.music.load("/".join([all_path if opened!=0 else audio_folder, str(selected_item)]))
        except error:
            messagebox.showerror('ERROR',get_error())
            next()
        else:
            mixer.music.load("/".join([all_path if opened!=0 else audio_folder, str(selected_item)]))

        paused = False
        mixer.music.play()
        main_slider.start()
        
def next():
    global paused
    cur_sel = song_list.curselection()
    paused = True
    last_item_index = song_list.size() - 1
    if cur_sel and int(cur_sel[-1]) == last_item_index:
        song_list.selection_clear(0, END)
        song_list.selection_set(0)
        play_music()
    else:
        song_list.selection_clear(0, END)
        song_list.selection_set(int(cur_sel[-1])+1)
        play_music()


def prev():
    global paused
    cur_sel = song_list.curselection()
    paused = True
    last_item_index = song_list.size() - 1
    if cur_sel and int(cur_sel[-1]) == 0:
        song_list.selection_clear(0, END)
        song_list.selection_set(last_item_index)
        play_music()
    else:
        song_list.selection_clear(0, END)
        song_list.selection_set(int(cur_sel[-1])-1)
        play_music()


def pause_music():
    global paused
    if paused == False:
        mixer.music.pause()
        main_slider.stop()
        paused = True
    
    elif paused:
        mixer.music.unpause()
        main_slider.start()
        paused = False



def del_music():
    index = song_list.curselection()
    if index:
        music_name = song_list.get(index)
        idx = song_list.get(0, END).index(music_name)
        song_list.delete(idx)
        remove("".join([all_path if all_path else audio_folder, str(music_name)]))

def find_audio():
    global audio_files
    global all_path
    global opened
    all_path = askdirectory(title='Select Music Folder',initialdir=audio_folder)
    audio_path = all_path if all_path else audio_folder
    opened+=1
    audio_extensions = (".mp3", ".wav")
    audio_files.clear()
    song_list.delete(0,END)
    for file in listdir(audio_path):
        if file.endswith(audio_extensions):
            audio_files.append((file))
    
    for i in audio_files:
        song_list.insert(END,i)

def about():
    about = Toplevel()
    about.geometry("438x276")
    about.title('About')
    about.iconbitmap(relative_to_assets('music.ico'))
    about.configure(bg = "#FFFFFF")
    canvas = Canvas(
        about,
        bg = "#FFFFFF",
        height = 278,
        width = 439,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        )
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        439.0,
        278.0,
        fill="#D9D9D9",
        outline="")
    image_image_1 = PhotoImage(
        file=relative_to_assets("bg_image.png"))
    image_1 = canvas.create_image(
        219.0,
        139.0,
        image=image_image_1
        )
    button_image_1 = PhotoImage(
        file=relative_to_assets("replit.png"))
    button_1 = Button(
        about,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open('https://www.replit.com/@TheHackerClown'),
        relief="flat"
        )
    button_1.place(
        x=308.0,
        y=43.0,
        width=77.580078125,
        height=74.13330078125
        )
    button_image_2 = PhotoImage(
        file=relative_to_assets("facebook.png"))
    button_2 = Button(
        about,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open('https://www.facebook.com/the.hacker.clown'),
        relief="flat"
        )
    button_2.place(
        x=196.0,
        y=43.0,
        width=77.580078125,
        height=74.13330078125
        )
    button_image_3 = PhotoImage(
        file=relative_to_assets("github.png"))
    button_3 = Button(
        about,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:webbrowser.open('https://github.com/TheHackerClown'),
        relief="flat"
        )
    button_3.place(
        x=196.0,
        y=156.0,
        width=77.580078125,
        height=74.13330078125
        )
    button_image_4 = PhotoImage(
        file=relative_to_assets("instagram.png"))
    button_4 = Button(
        about,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:webbrowser.open('https://instagram.com/the.hacker.clown'),
        relief="flat"
        )
    button_4.place(
        x=308.0,
        y=156.0,
        width=77.580078125,
        height=74.13330078125
        )
    about.resizable(False, False)
    about.mainloop()

def settings():
    setting = Toplevel()
    setting.title('Coming Soon....')
    setting.iconbitmap(relative_to_assets('music.ico'))
    setting.configure(bg = "#FFFFFF")
    button_image_4 = PhotoImage(
        file=relative_to_assets("hehe.png"))
    button_4 = Button(
        setting,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda:messagebox.showerror('404','bade harami ho beta 💀🐱‍💻')
        )
    button_4.pack()
    setting.resizable(False, False)
    setting.mainloop()




window = Tk()
window.title('Taby - Music Player')
window.iconbitmap(relative_to_assets('music.ico'))
window.geometry("801x439")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
     window,
    bg = "#FFFFFF",
    height = 439,
    width = 801,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)


'''BACKGROUND IMAGE'''
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    219.0,
    image=image_image_1
)


'''Setting Button'''
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:settings(),
    relief="flat"
)
button_1.place(
    x=13.0,
    y=122.0,
    width=95.0,
    height=48.0
)

'''About Button'''
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: about(),
    relief="flat"
)
button_2.place(
    x=13.0,
    y=195.0,
    width=95.0,
    height=48.0
)


'''Home Button'''
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: settings(),
    relief="flat"
)
button_3.place(
    x=13.0,
    y=46.0,
    width=95.0,
    height=48.0
)


'''Open File Button'''
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: find_audio(),
    relief="flat"
)
button_4.place(
    x=150.0,
    y=346.0,
    width=128.0,
    height=48.0
)

'''Delete Button'''
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: del_music(),
    relief="flat"
)
button_5.place(
    x=150.0,
    y=277.0,
    width=128.0,
    height=48.0
)


'''Play Selected Button'''
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_music(),
    relief="flat"
)
button_6.place(
    x=150.0,
    y=206.0,
    width=128.0,
    height=48.0
)



'''SONG LIST BOX [Working]'''
song_list = Listbox(
    window,
    height=15,
    width=79,
    fg='#FF4141',
    bg='#353737',
    relief='flat')
audio_extensions = (".mp3", ".wav")
for file in listdir(audio_folder):
    if file.endswith(audio_extensions):
        audio_files.append((file))
song_list.delete(0,END)
for i in audio_files:
        song_list.insert(END,i)
song_list.place(x=301,y=180)
scroll = CTkScrollbar(window,height=242,bg_color='#353737',button_color='#ff4141',command=song_list.yview)
song_list.config(yscrollcommand=scroll.set)
scroll.place(x=762,y=181)

'''Volume Slider [Condition-Working]'''
current_volume=0
for session in sessions:
    volume = session.SimpleAudioVolume
    if session.Process and session.Process.name() == "explorer.exe":
        current_volume = volume.GetMasterVolume()
        break
style = Style()
def set_volume(value):
    mixer.music.set_volume(float(value))
style.configure("Horizontal.TScale", background="#353737", fg='#ff4141',troughcolor="#ff4141", sliderlength=20)
volume_slider = Scale(window, from_=0, to=1, orient=HORIZONTAL,command=set_volume ,length=120)
volume_slider.place(x=666,y=80)

'''MAIN MUSIC SLIDER [CONDITION-Working]'''
def set_music_pos(value):
    mixer.music.set_pos(value)

main_slider = CTkSlider(window,
                        width=470,
                        orientation='horizontal',
                        bg_color='#353737',
                        button_color='#353737',
                        button_hover_color='#ff4141',
                        progress_color='#ff4141',
                        command=set_music_pos
                        )
main_slider.place(x=310,y=50)
main_slider.set(0)

'''Play Button [Condition-Working]'''
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:pause_music(),
    relief="flat"
)
button_7.place(
    x=501.0,
    y=74.0,
    width=70.0,
    height=70.0
)
window.bind('<space>',lambda event:pause_music())


'''Previous Button [Condition-Working]'''
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: prev(),
    relief="flat"
)
button_8.place(
    x=436.0,
    y=85.0,
    width=50.0,
    height=50.0
)
window.bind('<Left>',lambda event:prev())

'''Next Button [Condition-Working]'''
button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: next(),
    relief="flat"
)
button_9.place(
    x=592.0,
    y=83.0,
    width=50.0,
    height=50.0
)   
window.bind('<Right>',lambda event:next())


'''Song Name Label [Condition-Working]'''
Song_name=canvas.create_text(320,28,font=('Times New Roman',16,'bold'),fill='#ff4141',tags=("marquee",),anchor='w')
window.resizable(False, False)
window.mainloop()

from customtkinter import CTkButton,CTkEntry,CTkFrame,CTkScrollableFrame,CTkLabel,CTkSlider,set_default_color_theme,CTk,CTkTabview,CTkImage,set_appearance_mode

set_default_color_theme('Data/theme.json')

class MenuFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.home = CTkButton(self,text='Home')
        self.home.grid(row=0, column=0, padx=10,pady=10,sticky='ew')
        self.setting = CTkButton(self,text='Setting')
        self.setting.grid(row=1,column=0,padx=10,pady=10,sticky='ew')
        self.about = CTkButton(self,text='About')
        self.about.grid(row=2,column=0,padx=10,pady=10,sticky='ew')


class MusicListFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

class App:
    def __init__(self):
        from PIL import Image
        self = CTk()
        self.title('Music Player')
        global values
        values = 0

        #side menu
        self.my_frame = MenuFrame(master=self)
        self.my_frame.grid(row=0,column=0,sticky='ns')
        
        #tab view
        self.tabview = CTkTabview(master=self)
        self.tabview.grid(row=0,column=1,padx=20,pady=20)
        self.tabview.add('Player')
        self.tabview.add('Songs')
        self.tabview.set('Player')
        
        #album art
        self.album_img = CTkImage(dark_image=Image.open("Data/default.png"),size=(150, 150))
        self.label = CTkLabel(self.tabview.tab('Player'),text='', image=self.album_img)
        self.label.pack(pady=10)
        
        #slider music control
        def slider_event(value):
            global values
            values=value
        self.slider = CTkSlider(master=self.tabview.tab('Player'), from_=0, to=100,command=slider_event)
        self.slider.pack(pady=10)
        
        #pause button
        self.pause = CTkImage(dark_image=Image.open("Data/pause.png"),size=(50, 50))
        self.button = CTkButton(master=self.tabview.tab('Player'),image=self.pause, command=lambda:print(values),text="")
        self.button.pack(pady=10)

        
        #play button
        self.play = CTkImage(dark_image=Image.open("Data/play.png"),size=(50, 50))
        self.button = CTkButton(master=self.tabview.tab('Player'),image=self.play, command=lambda:print(values),text="")
        self.button.pack(pady=10)

        #setup
        set_appearance_mode('dark')
        self.resizable(False,False)
        self.mainloop()  

app = App()
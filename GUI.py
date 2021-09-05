from Discography import Discography
from contracts import DiscographyInterface
from tkinter import *


class DiscographyGUI:
    discography: DiscographyInterface
    window: Tk
    selected_album_index: int

    def __init__(self, file_name):
        self.discography = Discography()
        self.discography.load(file_name)
        self.window = Tk()
        self.window.geometry("1280x720")
        self.children_list = []

    def open(self):
        self.window.title("DiscographyGUI")
        title = Label(self.window, text="discography", fg="blue", font=("Helvetica", 49))
        title.place(relx=0.5, rely=0.05, anchor='n')
        self.open_window()
        self.window.mainloop()

    def open_window(self):
        self.clear_window()
        self.return_button("EXIST", self.window.quit)
        relx = 0.2
        rely = 0.4
        button1 = Button(text="Search", fg="green", bg="grey81", font=("Helvetica", 32), command=self.queries)
        button1.place(relx=relx, rely=rely, anchor=NW)
        relx = 0.6
        button2 = Button(text="Albums", fg="green", bg="grey81", font=("Helvetica", 32), command=self.albums)
        button2.place(relx=relx, rely=rely, anchor=NW)
        self.children_list.append(button1)
        self.children_list.append(button2)



    def queries(self):
        self.clear_window()
        rely = 0.25
        relx = 0.15
        text_result = Text(self.window)
        OPTIONS = [
            "album",
            "find song album",
            "song length",
            "song lyrics",
            "song length",
            "search song",
            "search song by lyrics"
        ]

        def resulat():
            command = variable.get()
            command_phrase = search_box.get("1.0", "end").replace("\n","")
            if command == "album":
                result = self.discography.get_songs(album=command_phrase)
            elif command == "song length":
                result = self.discography.get_song_len(song_name=command_phrase)
            elif command == "song lyrics":
                result = self.discography.get_lyrics(song_name=command_phrase)
            elif command == "find song album":
                result = self.discography.find_album(song_name=command_phrase)
            elif command == "search song":
                result = self.discography.search_songs(phrase=" " + command_phrase.lower() + " ")
            elif command == "search song by lyrics":
                result = self.discography.search_by_lyrics(phrase=" " + command_phrase.lower())
            text_result.delete('1.0', END)
            text_result.insert(INSERT, result)
            text_result.place(relx=0.5, rely=0.5, anchor='n',height = 300)

        search_box = Text(self.window,height=1,width= 40, font = ("Helvetica", 16))
        search_box.place(relx=relx, rely=rely, anchor=NW)
        relx += 0.4
        rely -=0.01
        variable = StringVar(self.window)
        variable.set(OPTIONS[0])
        option_menu = OptionMenu(self.window, variable, *OPTIONS)
        option_menu.config(font = ("Helvetica", 16), width=17)
        option_menu.config(bg="gray81", fg="white")
        option_menu['menu'].config(font = ("Helvetica", 16))
        option_menu.place(relx=relx, rely=rely, anchor=NW)
        relx += 0.2
        button = Button(text="search", fg="blue", bg="grey81",font = ("Helvetica", 16), command=resulat)
        button.place(relx=relx, rely=rely, anchor=NW)
        self.return_button("return",self.open_window)
        self.children_list.append(text_result)
        self.children_list.append(option_menu)
        self.children_list.append(search_box)
        self.children_list.append(button)


    def albums(self):
        self.clear_window()
        self.sub_title("Albums:")
        self.return_button("return", self.open_window)
        num_of_albums = len(self.discography.albums)
        rely = 0.2
        relx = 0.1
        for index in range(num_of_albums):
            rely = rely + 0.1

            command = lambda album_index=index: self.open_songs_list(album_index)
            button = Button(text=(self.discography.albums[index].name + ", " + self.discography.albums[index].year),
                            fg="blue", bg="grey", font=("Helvetica", 12), command=command)
            button.place(relx=relx, rely=rely, anchor=NW)
            self.children_list.append(button)
            if rely > 0.8:
                relx = relx + 0.3
                rely = 0.2

    def open_songs_list(self, album_index: int):
        self.clear_window()
        self.sub_title(self.discography.albums[album_index].name + " :")
        self.return_button("return", self.albums)
        rely = 0.25
        relx = 0.15
        for index in range(len(self.discography.albums[album_index].songs)):
            rely = rely + 0.05
            command = lambda album_index=album_index, song_index=index: self.open_song(album_index=album_index,
                                                                                       song_index=song_index)
            button = Button(text=(self.discography.albums[album_index].songs[index].name), fg="cyan", bg="grey",
                            font=("Helvetica", 11), command=command)
            button.place(relx=relx, rely=rely, anchor=NW)
            self.children_list.append(button)

    def open_song(self, album_index, song_index):
        self.clear_window()
        song = self.discography.albums[album_index].songs[song_index]
        label = Label(self.window, text="Singer: " + song.singer, fg="blue", font=("Helvetica", 14))
        self.children_list.append(label)
        label = Label(self.window, text="Length: " + song.length, fg="blue", font=("Helvetica", 14))
        self.children_list.append(label)
        label = Label(self.window, text="Album: " + song.album, fg="blue", font=("Helvetica", 14))
        self.children_list.append(label)
        command = lambda album_index=album_index, song_index=song_index: self.open_lyrics(album_index, song_index)
        button = Button(text="lyrics", fg="blue", bg="grey",
                        font=("Helvetica", 11), command=command)
        self.children_list.append(button)
        rely = 0.25
        relx = 0.15
        for child in self.children_list:
            child.place(relx=relx, rely=rely, anchor=NW)
            rely += 0.1
        self.sub_title(song.name + ":")
        self.return_button("return", lambda album_index=album_index: self.open_songs_list(album_index=album_index))

    def open_lyrics(self, album_index, song_index):
        self.clear_window()
        self.sub_title(self.discography.albums[album_index].songs[song_index].name + " lyrics:")
        lyrics = Text(self.window)
        self.return_button("return", lambda album_index=album_index: self.open_songs_list(album_index=album_index))
        lyrics_start_location = self.discography.albums[album_index].songs[song_index].lyrics_start_location
        lyrics_end_location = self.discography.albums[album_index].songs[song_index].lyrics_end_location
        lyrics_text = self.discography.database[lyrics_start_location:lyrics_end_location]
        lyrics.insert(INSERT, lyrics_text)
        lyrics.config(state=DISABLED)
        rely = 0.25
        relx = 0.15
        lyrics.place(relx=relx, rely=rely, anchor=NW)
        self.children_list.append((lyrics))

    def clear_window(self):
        for widgets in self.children_list:
            widgets.destroy()
        self.children_list.clear()

    def sub_title(self, sub_title):
        title = Label(self.window, text=sub_title, fg="green", font=("Helvetica", 32), anchor='center', padx=20)
        title.place(relx=0.1, rely=0.15, anchor=NW, bordermode=OUTSIDE)
        self.children_list.append(title)

    def return_button(self, title, command):
        return_button = Button(text=title, command=command, fg="red", bg="black",font=("Helvetica", 18))
        return_button.place(relx=0.9, rely=0.9)
        self.children_list.append(return_button)


gui = DiscographyGUI("Pink_Floyd_DB.txt")
gui.open()

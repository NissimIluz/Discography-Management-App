import string
from Discography import Discography
from contracts import DiscographyInterface


class DiscographyCMD:
    discography: DiscographyInterface

    def __init__(self, file_name):
        self.discography = Discography()
        self.discography.load(file_name)

    def open_command_line(self):
        action: string = ""
        help_list = ("\t\033[93malbums: \033[92mto get \n"
                     "\t\033[93malbum: \033[92mto get \n"
                     "\t\033[93mlength: \033[92mto get \n"
                     "\t\033[93mlyrics: \033[92mto get \n"
                     "\t\033[93mfind_song_album: \033[92mto get \n"
                     "\t\033[93msearch: \033[92mto get \n"
                     "\t\033[93msearch_by_lyrics: \033[92mto get \n"
                     )

        while action != "exit":
            action = input("\033[94mdiscography: ") + " "
            index = action.index(" ")
            command = action[0:index]
            command_phrase = action[index + 1:len(action)].strip()
            response: string

            if command == "albums":
                response = self.discography.get_albums()
            elif command == "album":
                response = self.discography.get_songs(album=command_phrase)
            elif command == "length":
                response = self.discography.get_song_len(song_name=command_phrase)
            elif command == "lyrics":
                response = self.discography.get_lyrics(song_name=command_phrase)
            elif command == "find_song_album":
                response = self.discography.find_album(song_name=command_phrase)
            elif command == "search":
                response = self.discography.search_songs(phrase=" " + command_phrase.lower() + " ")
            elif command == "search_by_lyrics":
                response = self.discography.search_by_lyrics(phrase=" " + command_phrase.lower())
            elif command == "help":
                response = help_list
            elif command.lower() == "exit":
                break
            else:
                response = "Try again. for more information write \033[91m'help'"
            print("\033[92m" + response)


cmd = DiscographyCMD("Pink_Floyd_DB.txt")
cmd.open_command_line()

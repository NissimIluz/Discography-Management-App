import string
from difflib import SequenceMatcher
from contracts import DiscographyInterface
from Song import Song
from Albums import Album


class Discography (DiscographyInterface):
    albums: Album = []
    songs: Song = []
    database: string

    def load(self, fileName):
        index: int = 0
        albums_index: int = -1
        new_song: Song = Song()
        pointer = open(fileName, "r")
        self.database = pointer.read()
        pointer.close
        while index < len(self.database):
            try:
                next_line = self.database.index("\n", index)
            except:
                break
            if self.database[index] == "#":
                index += 1
                self.albums.append(Album())
                albums_index += 1
                self.albums[albums_index].name, self.albums[albums_index].year = self.database[
                                                                                 index:next_line].split("::")
                self.albums[albums_index].songs = []

            elif self.database[index] == "*":
                new_song.lyrics_end_location = index
                self.albums[albums_index].songs.append(new_song)
                self.songs.append(new_song)
                index += 1
                new_song = Song()
                new_song.name, new_song.singer, new_song.length, search = self.database[index: next_line].split("::")
                new_song.album = self.albums[albums_index].name
                new_song.lyrics_start_location = self.database.index(search, index)
            index = next_line + 1

        new_song.lyrics_end_location = index-1
        self.albums[albums_index].songs.append(new_song)
        self.songs.append(new_song)
        del self.songs[0]
        del self.albums[0].songs[0]
        self.albums.sort(key=lambda album: album.name)
        self.songs.sort(key=lambda song: song.name)

    def get_albums(self):
        retval = ""
        for a in self.albums:
            retval = retval  + a.name + ", " + a.year + "\n"
        return retval

    def get_songs(self, album: string):
        return self.binary_search(album,self.albums, lambda index:  self.get_name_list(self.albums[index].songs))

    def get_name_list(self, songs):
        retval = ""
        for song in songs:
            retval = retval + song.name + "\n"
        return retval

    def get_song_len(self,song_name):
        return self.binary_search(song_name, self.songs,fonction = lambda index: self.songs[index].length)


    def find_album(self,song_name):
        return self.binary_search(song_name, self.songs,fonction =lambda index: self.songs[index].album)


    def get_lyrics(self,song_name):
        return self.binary_search(song_name, self.songs,fonction =lambda index:self.database[self.songs[index].lyrics_start_location : self.songs[index].lyrics_end_location])


    def search_songs(self,phrase):
        MIN_SCORE = 0.4
        matches = []
        for song in self.songs:
            score = self.match(phrase_to_search = phrase, search_in= song.name,score_function = lambda x,y: SequenceMatcher(lambda x: "\n", x, y).ratio())
            if score >= MIN_SCORE:
                matches.append([score,song.name])
        return self.get_songs_result(len(matches),matches)

    def search_by_lyrics(self, phrase):
        min_score = 0.7
        max_result = 15
        retval: string
        matches = []
        for song in self.songs:
            self.database[song.lyrics_start_location: song.lyrics_end_location]
            score = self.match(phrase_to_search = phrase.replace(" ",""), search_in= self.database[song.lyrics_start_location: song.lyrics_end_location].replace(" ",""),score_function = lambda x,y: SequenceMatcher(lambda x: "\n", x, y).quick_ratio())
            if score >= min_score:
                matches.append([score, song.name])
        index = min(max_result, len(matches))
        return self.get_songs_result(index, matches)

    def match(self, phrase_to_search:string, search_in:string, score_function):
        max_score = 0.0
        k:int = len(phrase_to_search)
        index: int = 0
        search_in = " "+search_in.lower().replace("\n","") +" "
        search_in_length = len(search_in)
        while index+k < search_in_length+1:
            score = score_function(phrase_to_search, search_in[index: (index + k)])
            if score > max_score:
                max_score = score
                if max_score == 1:
                    break
            index += 1
        return max_score

    def get_songs_result(self, index,matches):
        retval = ""
        if index==0:
            retval = "No results found"
        else:
            matches.sort(key=lambda x: x[0])
            while index > 0:
                index -= 1
                retval = retval + matches[index][1] + "\n"
        return retval

    def binary_search(self, phrase, search_in,fonction):
        left, right = 0,len(search_in)-1
        mid: int
        while left <= right:
            mid = int((right + left) / 2)
            if search_in[mid].name == phrase:
                return fonction(mid)
            elif phrase < search_in[mid].name:
                right = mid - 1
            else:
                left = mid + 1
        return "not found"



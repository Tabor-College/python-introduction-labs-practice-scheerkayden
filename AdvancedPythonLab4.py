class Song:
    
    #Song data is private using __
    #controlled access via methods
    #static variable tracking total songs

    total_songs = 0 #static variable
    
    def __init__(self, song_id, title, artist, duration):
        self.__song_id = song_id
        self.__title = title
        self.__artist = artist
        self.__duration = duration
        self.__play_count = 0

        Song.total_songs +=1

    def get_title(self):
        return self.__title
    
    def get_artist(self):
        return self.__artist
    
    def set_duration(self, new_duration):
        if new_duration > 0:
            self.__duration = new_duration
            return True
        print("Duration must be positive")
        return False
    
    def __increment_plays(self):
        self.__play_count +=1

    def play(self):
        self.__increment_plays()
        print(f"Playing: {self.__title} (Plays: {self.__play_count})")

    @staticmethod
    def get_total_songs():
        return Song.total_songs
    
class Playlist:

    #Playlist stores Song objects
    #Objects are passed to methods
    #Demonstrates composition

    def __init__(self, name, creator):
        self.__name = name
        self.__creator = creator
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)
        print(f"{song.get_title()} added to {self.__name}")

    def display(self):
        print(f"\nPlaylist: {self.__name}")
        for i, song in enumerate(self.songs, 1):
            print(f"{i}. {song.get_title()} - {song.get_artist()}")

class User:

    #sensitive data is private
    #validation protects balance
    #User owns Playlist objects

    total_users = 0

    def __init__(self, username, email, balance):
        self.__username = username
        self.__email = email
        self.__balance = balance
        self.__playlists = []

        User.total_users +=1

    def pay_for_premium(self, cost):
        if cost <= self.__balance:
            self.__balance -= cost
            print("Premium activated!")
            return True
        print("Insufficient balance!")
        return False
    
    def create_playlist(self, name):
        playlist = Playlist(name, self.__username)
        self.__playlists.append(playlist)
        return playlist
    
    @staticmethod
    def get_total_users():
        return User.total_users
    
#Create Song objects
song1 = Song(101, "Pour Some Sugar on Me", "Def Leppard", 268)
song2 = Song(102, "Stormtroopers", "Sabaton", 236)

print("Total Songs:", Song.get_total_songs())

#Play a song
song1.play()
song1.play()

#Create user
user1 = User("Kayden", "kayden@soptify.com", 500)

#Create Playlist
rock = user1.create_playlist("Rock")

#Add Song objects to Playlist
rock.add_song(song1)
rock.add_song(song2)

#Display Playlist
rock.display()

#Pay for premium
user1.pay_for_premium(200)

#Objects are created using contructors
#methods are called on objects using dots
#private data is never directly accessed
#objects interact with other objects

#----------------------------------------------------------------------Advanced Spotify Lab-------------------------------------------------------------------------#

def playback_logger(func):
    """Decorator: Adds logging around playback"""
    def wrapper(self):
        print(" Logging playback...")
        result = func(self)
        print(" Playback complete\n")
        return result
    return wrapper

class Song:
    total_songs = 0 #static variable
    
    def __init__(self, song_id, title, artist, duration):
        self.__song_id = song_id
        self.__title = title
        self.__artist = artist
        self.__duration = duration
        self.__play_count = 0

        Song.total_songs +=1

    def get_title(self):
        return self.__title
    
    def get_artist(self):
        return self.__artist
    
    def __increment_plays(self):
        self.__play_count +=1

    @playback_logger
    def play(self):
        self.__increment_plays()
        print(f"Playing: {self.__title} ({self.__play_count})")

    #decorator wraps behavior without changing logic
    #encapsulation protects song state

class Playlist:

    #Iterator enables: for song in playlist
    #generator streams songs lazily
    #duck typing depends on behavior, not type

    def __init__(self, name):
        self.__name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __iter__(self):
        """Iterator entry point"""
        self._index = 0
        return self
    
    def __next__(self):
        """Iterator control"""
        if self._index >=len(self.songs):
            raise StopIteration
        song = self.songs[self._index]
        self._index +=1
        return song
    
    def play_songs(self):
        """Generator: Yields songs one at a time"""
        for song in self.songs:
            yield song

    def play_all(self, player):
        """Duck Typing: Any object with a play() method works"""
        for song in self:
            player.play(song)

def playback_limiter(max_plays):
    """Closure: remembers play count across calls"""
    count = 0

    def limiter(song):
        nonlocal count
        if count < max_plays:
            song.play()
            count +=1
        else:
            print(" Playback limit reached")
    return limiter

#Inner function remembers outer state
#no class required
#Function behaves like an object

class SimplePlayer:
    def play(self, song):
        song.play()

class LimitedPlayer:

    #Playlist doesn't care about player type
    #only requirement: play(song) method
    def __init__(self, limiter):
        self.limiter = limiter

    def play(self, song):
        self.limiter(song)

#Songs
s1 = Song(101, "Pour Some Sugar on Me", "Def Leppard", 268)
s2 = Song(102, "Stormtroopers", "Sabaton", 236)

#Playlist
rock = Playlist("rock")
rock.add_song(s1)
rock.add_song(s2)

#Closure
limit_1 = playback_limiter(1)

#Players
normal_player = SimplePlayer()
limited_player = LimitedPlayer(limit_1)

#Duck Typing in action
rock.play_all(normal_player)
rock.play_all(limited_player)

#Iterator drives looping
#Generator controls flow
#Decorator wraps logic
#closure preserves state
#Duck typing enables flexibility
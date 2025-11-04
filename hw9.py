class TV:
    def on(self):
        print("TV on")

    def off(self):
        print("TV off")

    def set_channel(self, channel):
        print(f"TV channel set to {channel}")

class AudioSystem:
    def on(self):
        print("AudioSystem on")

    def off(self):
        print("AudioSystem off")

    def set_volume(self, level):
        print(f"Volume set to {level}")

class DVDPlayer:
    def play(self):
        print("DVD playing")

    def pause(self):
        print("DVD paused")

    def stop(self):
        print("DVD stopped")

class GameConsole:
    def on(self):
        print("GameConsole on")

    def start_game(self):
        print("Game started")

class HomeTheaterFacade:
    def __init__(self):
        self.tv = TV()
        self.audio = AudioSystem()
        self.dvd = DVDPlayer()
        self.game = GameConsole()

    def watch_movie(self):
        self.tv.on()
        self.audio.on()
        self.audio.set_volume(5)
        self.tv.set_channel("HDMI1")
        self.dvd.play()

    def stop_movie(self):
        self.dvd.stop()
        self.tv.off()
        self.audio.off()

    def play_game(self):
        self.tv.on()
        self.audio.on()
        self.tv.set_channel("HDMI2")
        self.game.on()
        self.game.start_game()

    def listen_music(self):
        self.tv.on()
        self.audio.on()
        self.tv.set_channel("AUX")

    def set_volume(self, level):
        self.audio.set_volume(level)

class FileSystemComponent:
    def display(self):
        pass

    def get_size(self):
        pass

class File(FileSystemComponent):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def display(self):
        print(f"File: {self.name} ({self.size} KB)")

    def get_size(self):
        return self.size

class Directory(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.contents = []

    def add(self, component):
        if component not in self.contents:
            self.contents.append(component)

    def remove(self, component):
        if component in self.contents:
            self.contents.remove(component)

    def display(self):
        print(f"Directory: {self.name}")
        for c in self.contents:
            c.display()

    def get_size(self):
        return sum(c.get_size() for c in self.contents)

theater = HomeTheaterFacade()
theater.watch_movie()
theater.set_volume(7)
theater.stop_movie()
theater.play_game()
theater.listen_music()

root = Directory("root")
docs = Directory("documents")
img = Directory("images")
file1 = File("resume.pdf", 120)
file2 = File("photo.jpg", 300)
file3 = File("notes.txt", 80)

docs.add(file1)
docs.add(file3)
img.add(file2)
root.add(docs)
root.add(img)

root.display()
print(f"Total size: {root.get_size()} KB")

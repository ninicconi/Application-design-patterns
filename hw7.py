from abc import ABC, abstractmethod

class ICommand(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass


class Light:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"

    def on(self):
        self.state = "ON"
        print(f"{self.name} light is ON")

    def off(self):
        self.state = "OFF"
        print(f"{self.name} light is OFF")


class Door:
    def __init__(self, name):
        self.name = name
        self.state = "CLOSED"

    def open(self):
        self.state = "OPEN"
        print(f"{self.name} door is OPEN")

    def close(self):
        self.state = "CLOSED"
        print(f"{self.name} door is CLOSED")


class Thermostat:
    def __init__(self, name, temp=20):
        self.name = name
        self.temp = temp

    def set_temp(self, new_temp):
        print(f"{self.name} thermostat set to {new_temp}°C")
        self.temp = new_temp


class Television:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"

    def on(self):
        self.state = "ON"
        print(f"{self.name} TV is ON")

    def off(self):
        self.state = "OFF"
        print(f"{self.name} TV is OFF")


class LightOnCommand(ICommand):
    def __init__(self, light): self.light = light
    def execute(self): self.light.on()
    def undo(self): self.light.off()


class DoorOpenCommand(ICommand):
    def __init__(self, door): self.door = door
    def execute(self): self.door.open()
    def undo(self): self.door.close()


class ThermostatSetTempCommand(ICommand):
    def __init__(self, thermostat, temp):
        self.thermostat = thermostat
        self.new_temp = temp
        self.prev_temp = thermostat.temp
    def execute(self): self.thermostat.set_temp(self.new_temp)
    def undo(self): self.thermostat.set_temp(self.prev_temp)


class TVOnCommand(ICommand):
    def __init__(self, tv): self.tv = tv
    def execute(self): self.tv.on()
    def undo(self): self.tv.off()


class Invoker:
    def __init__(self):
        self.history = []

    def execute(self, command):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if not self.history:
            print("Nothing to undo.")
            return
        self.history.pop().undo()


class Beverage(ABC):
    def prepare(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.customer_wants_condiments():
            self.add_condiments()
        print("Drink ready.\n")

    def boil_water(self): print("Boiling water")
    def pour_in_cup(self): print("Pouring into cup")
    def customer_wants_condiments(self): return True

    @abstractmethod
    def brew(self): pass

    @abstractmethod
    def add_condiments(self): pass


class Tea(Beverage):
    def brew(self): print("Steeping the tea")
    def add_condiments(self): print("Adding lemon")


class Coffee(Beverage):
    def brew(self): print("Dripping coffee through filter")
    def add_condiments(self): print("Adding sugar and milk")


class HotChocolate(Beverage):
    def brew(self): print("Mixing cocoa powder with milk")
    def add_condiments(self): print("Adding whipped cream")


class IMediator(ABC):
    @abstractmethod
    def send(self, sender, message): pass

    @abstractmethod
    def register(self, user): pass


class ChatRoom(IMediator):
    def __init__(self):
        self.users = {}

    def register(self, user):
        self.users[user.name] = user
        user.mediator = self
        print(f"{user.name} joined the chat")

    def send(self, sender, message, receiver_name=None):
        if receiver_name:
            receiver = self.users.get(receiver_name)
            if receiver:
                receiver.receive(sender, message, private=True)
            else:
                print("User not found")
        else:
            for user in self.users.values():
                if user != sender:
                    user.receive(sender, message)


class User:
    def __init__(self, name):
        self.name = name
        self.mediator = None

    def send(self, message, receiver_name=None):
        if not self.mediator:
            print(f"{self.name} is not in chat")
            return
        self.mediator.send(self, message, receiver_name)

    def receive(self, sender, message, private=False):
        if private:
            print(f"[Private] {self.name} got from {sender.name}: {message}")
        else:
            print(f"{self.name} got from {sender.name}: {message}")


if __name__ == "__main__":
    light = Light("Living Room")
    door = Door("Front")
    thermostat = Thermostat("Main", 22)
    tv = Television("Bedroom")

    invoker = Invoker()
    invoker.execute(LightOnCommand(light))
    invoker.execute(DoorOpenCommand(door))
    invoker.execute(ThermostatSetTempCommand(thermostat, 25))
    invoker.execute(TVOnCommand(tv))
    invoker.undo_last()

    print("\nPreparing Tea:")
    tea = Tea()
    tea.prepare()

    print("Preparing Coffee:")
    coffee = Coffee()
    coffee.prepare()

    print("Preparing Hot Chocolate:")
    cocoa = HotChocolate()
    cocoa.prepare()

    print("\nChat System:")
    chat = ChatRoom()
    nika = User("Nika")
    niusha = User("Niusha")
    chat.register(nika)
    chat.register(niusha)

    nika.send("Hello everyone!")
    niusha.send("Hi Nika!")
    nika.send("How are you?", "Niusha")

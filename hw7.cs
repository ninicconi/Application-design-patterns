using System;
using System.Collections.Generic;


interface ICommand
{
    void Execute();
    void Undo();
}


class Light
{
    public void On() => Console.WriteLine("Light turned on");
    public void Off() => Console.WriteLine("Light turned off");
}

class Door
{
    public void Open() => Console.WriteLine("Door opened");
    public void Close() => Console.WriteLine("Door closed");
}

class Thermostat
{
    public void Increase() => Console.WriteLine("Temperature increased");
    public void Decrease() => Console.WriteLine("Temperature decreased");
}

class TV
{
    public void On() => Console.WriteLine("TV turned on");
    public void Off() => Console.WriteLine("TV turned off");
}


class LightCommand : ICommand
{
    private readonly Light light;
    private readonly bool on;
    public LightCommand(Light light, bool on) { this.light = light; this.on = on; }
    public void Execute() { if (on) light.On(); else light.Off(); }
    public void Undo() { if (on) light.Off(); else light.On(); }
}

class DoorCommand : ICommand
{
    private readonly Door door;
    private readonly bool open;
    public DoorCommand(Door door, bool open) { this.door = door; this.open = open; }
    public void Execute() { if (open) door.Open(); else door.Close(); }
    public void Undo() { if (open) door.Close(); else door.Open(); }
}

class TempCommand : ICommand
{
    private readonly Thermostat thermostat;
    private readonly bool increase;
    public TempCommand(Thermostat thermostat, bool increase) { this.thermostat = thermostat; this.increase = increase; }
    public void Execute() { if (increase) thermostat.Increase(); else thermostat.Decrease(); }
    public void Undo() { if (increase) thermostat.Decrease(); else thermostat.Increase(); }
}

class TVCommand : ICommand
{
    private readonly TV tv;
    private readonly bool on;
    public TVCommand(TV tv, bool on) { this.tv = tv; this.on = on; }
    public void Execute() { if (on) tv.On(); else tv.Off(); }
    public void Undo() { if (on) tv.Off(); else tv.On(); }
}


class Invoker
{
    private readonly Stack<ICommand> history = new();
    public void Run(ICommand command)
    {
        command.Execute();
        history.Push(command);
    }

    public void Undo()
    {
        if (history.Count > 0)
            history.Pop().Undo();
        else
            Console.WriteLine("No commands to undo");
    }
}


abstract class Beverage
{
    public void Prepare()
    {
        BoilWater();
        Brew();
        Pour();
        if (WantsCondiments()) AddCondiments();
    }

    private void BoilWater() => Console.WriteLine("Boiling water");
    private void Pour() => Console.WriteLine("Pouring into cup");

    protected abstract void Brew();
    protected abstract void AddCondiments();
    protected virtual bool WantsCondiments() => true;
}

class Tea : Beverage
{
    protected override void Brew() => Console.WriteLine("Steeping tea");
    protected override void AddCondiments() => Console.WriteLine("Adding lemon");
}

class Coffee : Beverage
{
    protected override void Brew() => Console.WriteLine("Brewing coffee");
    protected override void AddCondiments() => Console.WriteLine("Adding sugar and milk");

    protected override bool WantsCondiments()
    {
        Console.Write("Add condiments? (y/n): ");
        return Console.ReadLine()?.Trim().ToLower() == "y";
    }
}

class HotChocolate : Beverage
{
    protected override void Brew() => Console.WriteLine("Mixing cocoa");
    protected override void AddCondiments() => Console.WriteLine("Adding marshmallows");
}



interface IMediator
{
    void Send(string message, User sender);
    void SendPrivate(string message, User sender, string receiver);
    void Join(User user);
    void Leave(User user);
}

class ChatRoom : IMediator
{
    private readonly Dictionary<string, User> users = new();

    public void Join(User user)
    {
        users[user.Name] = user;
        Broadcast($"{user.Name} joined the chat", user);
    }

    public void Leave(User user)
    {
        if (users.Remove(user.Name))
            Broadcast($"{user.Name} left the chat", user);
    }

    public void Send(string message, User sender)
    {
        if (!users.ContainsKey(sender.Name))
        {
            Console.WriteLine($"{sender.Name} is not in the chat");
            return;
        }

        foreach (var u in users.Values)
            if (u != sender)
                u.Receive(message, sender.Name);
    }

    public void SendPrivate(string message, User sender, string receiver)
    {
        if (users.TryGetValue(receiver, out var user))
            user.Receive($"(private) {message}", sender.Name);
    }

    private void Broadcast(string message, User sender)
    {
        foreach (var u in users.Values)
            if (u != sender)
                u.Receive(message, "System");
    }
}

class User
{
    public string Name { get; }
    private readonly IMediator chat;

    public User(string name, IMediator chat)
    {
        Name = name;
        this.chat = chat;
    }

    public void Join() => chat.Join(this);
    public void Leave() => chat.Leave(this);
    public void Send(string message) => chat.Send(message, this);
    public void SendPrivate(string message, string to) => chat.SendPrivate(message, this, to);
    public void Receive(string message, string from) => Console.WriteLine($"{Name} received from {from}: {message}");
}


class Program
{
    static void Main()
    {
        var invoker = new Invoker();
        var light = new Light();
        var door = new Door();
        var temp = new Thermostat();
        var tv = new TV();

        invoker.Run(new LightCommand(light, true));
        invoker.Run(new DoorCommand(door, true));
        invoker.Run(new TempCommand(temp, true));
        invoker.Run(new TVCommand(tv, true));
        invoker.Undo();
        invoker.Undo();

        new Tea().Prepare();
        new Coffee().Prepare();
        new HotChocolate().Prepare();

        var room = new ChatRoom();
        var nika = new User("Nika", room);
        var niusha = new User("Niusha", room);
        var danel = new User("Danel", room);

        nika.Join();
        niusha.Join();
        danel.Join();

        nika.Send("Hi everyone!");
        niusha.SendPrivate("Hey Nika", "Nika");
        danel.Leave();
        danel.Send("Still here?");
    }
}

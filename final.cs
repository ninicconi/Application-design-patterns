 
#region Program

var tesla = new Asset("Tesla");

var email = new EmailNotification();
var sms = new SmsNotification();
var push = new PushNotification();

var privateInvestor = new PrivateInvestor(push);
var professionalInvestor = new ProfessionalInvestor(email);
var analyst = new FinancialAnalyst(sms);

tesla.Attach(privateInvestor);
tesla.Attach(professionalInvestor);
tesla.Attach(analyst);


tesla.Notify(new PriceChangeEvent("Tesla", "Tesla price changed to $800"));
tesla.Notify(new ThresholdEvent("Tesla", "Tesla reached sell threshold"));
tesla.Notify(new DividendEvent("Tesla", "Tesla announced dividend"));
tesla.Notify(new MarketAlertEvent("Market", "Market dropped by 5%"));


tesla.Detach(privateInvestor);

#endregion

#region Events

abstract class MarketEvent(string asset, string message)
{
    public string Asset = asset;
    public readonly string Message = message;
}

class PriceChangeEvent(string asset, string message) : MarketEvent(asset, message);

class ThresholdEvent(string asset, string message) : MarketEvent(asset, message);

class MarketAlertEvent(string asset, string message) : MarketEvent(asset, message);

class DividendEvent(string asset, string message) : MarketEvent(asset, message);

#endregion

#region Observer 

interface IObserver
{
    void Update(MarketEvent marketEvent);
}

#endregion

#region Subject

interface ISubject
{
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify(MarketEvent marketEvent);
}

#endregion

#region Notifications

interface INotificationChannel
{
    void Send(string message);
}

class EmailNotification : INotificationChannel
{
    public void Send(string message) =>
        Console.WriteLine("Email: " + message);
}

internal class SmsNotification : INotificationChannel
{
    public void Send(string message) =>
        Console.WriteLine("SMS: " + message);
}

class PushNotification : INotificationChannel
{
    public void Send(string message) =>
        Console.WriteLine("Push: " + message);
}

#endregion

#region User

abstract class User(INotificationChannel channel) : IObserver
{
    protected readonly INotificationChannel Channel = channel;

    public abstract void Update(MarketEvent marketEvent);
}

class PrivateInvestor(INotificationChannel channel) : User(channel)
{
    public override void Update(MarketEvent marketEvent)
    {
        if (marketEvent is PriceChangeEvent || marketEvent is ThresholdEvent)
            Channel.Send(marketEvent.Message);
    }
}

class ProfessionalInvestor(INotificationChannel channel) : User(channel)
{
    public override void Update(MarketEvent marketEvent) =>
        Channel.Send(marketEvent.Message);
}

class FinancialAnalyst(INotificationChannel channel) : User(channel)
{
    public override void Update(MarketEvent marketEvent) =>
        Channel.Send("Detailed report: " + marketEvent.Message);
}

#endregion

#region Aset

class Asset(string name) : ISubject
{
    private readonly List<IObserver> _observers = new();
    public string Name = name;

    public void Attach(IObserver observer) =>
        _observers.Add(observer);

    public void Detach(IObserver observer) =>
        _observers.Remove(observer);

    public void Notify(MarketEvent marketEvent)
    {
        foreach (var observer in _observers)
            observer.Update(marketEvent);
    }
}

#endregion

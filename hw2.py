class IPaymentStrategy:
    def pay(self, amount):
        pass


class BankCardPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount}$ using Bank Card.")


class PayPalPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount}$ using PayPal.")


class CryptoPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount}$ using Cryptocurrency.")


class PaymentContext:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def pay(self, amount):
        if self.strategy:
            self.strategy.pay(amount)
        else:
            print("No payment method selected.")


class IObserver:
    def update(self, rate):
        pass


class ISubject:
    def register_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observers(self):
        pass


class CurrencyExchange(ISubject):
    def __init__(self):
        self.observers = []
        self.rate = 0

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def set_rate(self, new_rate):
        self.rate = new_rate
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.rate)


class MobileApp(IObserver):
    def update(self, rate):
        print(f"[MobileApp] New rate: {rate}$")


class WebDashboard(IObserver):
    def update(self, rate):
        print(f"[WebDashboard] Rate displayed: {rate}$")


class AlertSystem(IObserver):
    def update(self, rate):
        if rate > 500:
            print(f"[AlertSystem] Warning! Rate too high: {rate}$")
        else:
            print(f"[AlertSystem] Rate is stable: {rate}$")


def main():
    context = PaymentContext()
    context.set_strategy(BankCardPayment())
    context.pay(150)
    context.set_strategy(PayPalPayment())
    context.pay(200)
    context.set_strategy(CryptoPayment())
    context.pay(300)

    exchange = CurrencyExchange()
    app = MobileApp()
    web = WebDashboard()
    alert = AlertSystem()

    exchange.register_observer(app)
    exchange.register_observer(web)
    exchange.register_observer(alert)

    exchange.set_rate(450)
    exchange.set_rate(520)
    exchange.set_rate(480)


if __name__ == "__main__":
    main()

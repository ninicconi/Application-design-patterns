import time

class PaymentStrategy:
    def pay(self, amount: float):
        raise NotImplementedError


class CardPayment(PaymentStrategy):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} with Card ending in {self.card_number[-4:]}.")


class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email

    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} via PayPal ({self.email}).")


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id

    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} BTC equivalent (Wallet ID: {self.wallet_id[:6]}...).")


class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def execute_payment(self, amount: float):
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        self.strategy.pay(amount)


class Currency:
    def __init__(self, name: str, rate: float):
        self.name = name
        self.rate = rate


class IObserver:
    def update(self, currency_data: Currency):
        raise NotImplementedError


class ISubject:
    def register_observer(self, observer: IObserver):
        raise NotImplementedError

    def remove_observer(self, observer: IObserver):
        raise NotImplementedError

    def notify_observers(self, currency_data: Currency):
        raise NotImplementedError


class CurrencyExchange(ISubject):
    def __init__(self):
        self.observers = []
        self.rates = {}

    def register_observer(self, observer: IObserver):
        self.observers.append(observer)
        print(f"{observer.name} subscribed to updates.")

    def remove_observer(self, observer: IObserver):
        if observer in self.observers:
            self.observers.remove(observer)
            print(f"{observer.name} unsubscribed.")
        else:
            print(f"{observer.name} not found in subscriber list.")

    def set_rate(self, name: str, new_rate: float):
        if new_rate <= 0:
            return
        self.rates[name] = Currency(name, new_rate)
        print(f"\nExchange rate for {name} updated to {new_rate:.4f}")
        self.notify_observers(self.rates[name])

    def notify_observers(self, currency_data: Currency):
        for observer in self.observers:
            observer.update(currency_data)


class SimpleDisplay(IObserver):
    def __init__(self, name="Mobile Screen"):
        self.name = name

    def update(self, currency_data: Currency):
        print(f"[{self.name}] {currency_data.name}: {currency_data.rate:.4f}")


class AlertSystem(IObserver):
    def __init__(self, name="Alert Bot", threshold=1.02):
        self.name = name
        self.threshold = threshold

    def update(self, currency_data: Currency):
        if currency_data.rate >= self.threshold:
            print(f"[{self.name}] ALERT: {currency_data.name} reached {currency_data.rate:.4f}!")


class DataLogger(IObserver):
    def __init__(self, name="Data Logger"):
        self.name = name
        self.history = []

    def update(self, currency_data: Currency):
        timestamp = time.strftime("%H:%M:%S")
        self.history.append((timestamp, currency_data.name, currency_data.rate))
        print(f"[{self.name}] Logged at {timestamp}.")


def run_strategy_test():
    print("=" * 50)
    print("PART 1: STRATEGY PATTERN TEST")
    print("=" * 50)

    card = CardPayment("6367220123456789")
    paypal = PayPalPayment("zhemeneynika@gmail.com")
    crypto = CryptoPayment("0xAaBc789012445678901275367890123456789012")
    processor = PaymentContext(card)

    print("\nTransaction 1: Card")
    processor.execute_payment(150.75)

    print("\nTransaction 2: PayPal")
    processor.set_strategy(paypal)
    processor.execute_payment(500.00)

    print("\nTransaction 3: Crypto")
    processor.set_strategy(crypto)
    processor.execute_payment(10.25)

    try:
        processor.execute_payment(-5.00)
    except ValueError as e:
        print(f"Error: {e}")


def run_observer_test():
    print("\n" + "=" * 50)
    print("PART 2: OBSERVER PATTERN TEST")
    print("=" * 50)

    exchange = CurrencyExchange()
    display = SimpleDisplay("Mobile Screen")
    alert = AlertSystem("Risk Bot", threshold=1.02)
    logger = DataLogger("Audit System")

    exchange.register_observer(display)
    exchange.register_observer(alert)
    exchange.register_observer(logger)

    print("\nUpdate 1: Small Change")
    exchange.set_rate("EUR/USD", 1.0100)

    print("\nUpdate 2: Large Change - Triggers Alert")
    exchange.set_rate("EUR/USD", 1.0550)

    print("\nRemoving Display Observer")
    exchange.remove_observer(display)

    print("\nUpdate 3: After Removal")
    exchange.set_rate("EUR/USD", 1.0400)


if __name__ == "__main__":
    run_strategy_test()
    run_observer_test()

class Beverage:
    def get_description(self):
        return "Unknown"

    def cost(self):
        return 0.0

class Espresso(Beverage):
    def get_description(self):
        return "Espresso"

    def cost(self):
        return 2.0

class Tea(Beverage):
    def get_description(self):
        return "Tea"

    def cost(self):
        return 1.5

class Latte(Beverage):
    def get_description(self):
        return "Latte"

    def cost(self):
        return 2.5

class Mocha(Beverage):
    def get_description(self):
        return "Mocha"

    def cost(self):
        return 3.0

class BeverageDecorator(Beverage):
    def __init__(self, beverage):
        self.beverage = beverage

class Milk(BeverageDecorator):
    def get_description(self):
        return self.beverage.get_description() + ", Milk"

    def cost(self):
        return self.beverage.cost() + 0.5

class Sugar(BeverageDecorator):
    def get_description(self):
        return self.beverage.get_description() + ", Sugar"

    def cost(self):
        return self.beverage.cost() + 0.2

class WhippedCream(BeverageDecorator):
    def get_description(self):
        return self.beverage.get_description() + ", Whipped Cream"

    def cost(self):
        return self.beverage.cost() + 0.7

class IPaymentProcessor:
    def process_payment(self, amount):
        pass

class PayPalPaymentProcessor(IPaymentProcessor):
    def process_payment(self, amount):
        print(f"Paid {amount:.2f} with PayPal")

class StripePaymentService:
    def make_transaction(self, total_amount):
        print(f"Paid {total_amount:.2f} with Stripe")

class StripePaymentAdapter(IPaymentProcessor):
    def __init__(self):
        self.stripe = StripePaymentService()

    def process_payment(self, amount):
        self.stripe.make_transaction(amount)

class AnotherPaymentService:
    def pay(self, value):
        print(f"Paid {value:.2f} with AnotherService")

class AnotherPaymentAdapter(IPaymentProcessor):
    def __init__(self):
        self.service = AnotherPaymentService()

    def process_payment(self, amount):
        self.service.pay(amount)

drink = Mocha()
drink = Milk(drink)
drink = Sugar(drink)
drink = WhippedCream(drink)

print(drink.get_description())
print(f"Total: {drink.cost():.2f}")

processors = [
    PayPalPaymentProcessor(),
    StripePaymentAdapter(),
    AnotherPaymentAdapter()
]

for processor in processors:
    processor.process_payment(drink.cost())

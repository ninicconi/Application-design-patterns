from abc import ABC, abstractmethod

class Order:
    def __init__(self, product_name, quantity, price):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price


class PriceCalculator:
    def calculate_total(self, order):
        return order.quantity * order.price * 0.9


class PaymentProcessor:
    def process(self, payment_method):
        print(f"Payment processed using {payment_method}")


class Notifier:
    def send_confirmation(self, email):
        print(f"Confirmation email sent to {email}")


class Employee(ABC):
    def __init__(self, base_salary):
        self.base_salary = base_salary

    @abstractmethod
    def calculate_salary(self):
        pass


class PermanentEmployee(Employee):
    def calculate_salary(self):
        return self.base_salary * 1.2


class ContractEmployee(Employee):
    def calculate_salary(self):
        return self.base_salary * 1.1


class Intern(Employee):
    def calculate_salary(self):
        return self.base_salary


class SalaryCalculator:
    def get_salary(self, employee: Employee):
        return employee.calculate_salary()


class IPrinter(ABC):
    @abstractmethod
    def print(self, content):
        pass


class IScanner(ABC):
    @abstractmethod
    def scan(self, content):
        pass


class IFax(ABC):
    @abstractmethod
    def fax(self, content):
        pass


class BasicPrinter(IPrinter):
    def print(self, content):
        print(f"Printing: {content}")


class MultiFunctionPrinter(IPrinter, IScanner, IFax):
    def print(self, content):
        print(f"Printing: {content}")

    def scan(self, content):
        print(f"Scanning: {content}")

    def fax(self, content):
        print(f"Faxing: {content}")


class IMessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailSender(IMessageSender):
    def send(self, message):
        print(f"Email sent: {message}")


class SmsSender(IMessageSender):
    def send(self, message):
        print(f"SMS sent: {message}")


class NotificationService:
    def __init__(self, sender: IMessageSender):
        self.sender = sender

    def notify(self, message):
        self.sender.send(message)


def main():
    order = Order("Laptop", 2, 800)
    calculator = PriceCalculator()
    print("Total price:", calculator.calculate_total(order))
    processor = PaymentProcessor()
    processor.process("Bank Card")
    notifier = Notifier()
    notifier.send_confirmation("zhemeneynika@gmail.com")

    employee1 = PermanentEmployee(1000)
    employee2 = ContractEmployee(800)
    salary_calc = SalaryCalculator()
    print("Permanent employee salary:", salary_calc.get_salary(employee1))
    print("Contract employee salary:", salary_calc.get_salary(employee2))

    printer = BasicPrinter()
    printer.print("Test Document")
    mfp = MultiFunctionPrinter()
    mfp.print("Invoice")
    mfp.scan("Report")
    mfp.fax("Contract")

    email_sender = EmailSender()
    sms_sender = SmsSender()
    email_notifier = NotificationService(email_sender)
    sms_notifier = NotificationService(sms_sender)
    email_notifier.notify("Your order has been shipped!")
    sms_notifier.notify("Payment received successfully!")


if __name__ == "__main__":
    main()

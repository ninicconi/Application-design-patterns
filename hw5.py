import threading
import os
import copy
from abc import ABC, abstractmethod


class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()
    _file_path = "config.txt"

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._settings = {}
        self.load_settings()
        self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def load_settings(self):
        if not os.path.exists(self._file_path):
            self._settings = {"log_level": "INFO", "max_threads": "4"}
            self.save_settings()
            return
        with open(self._file_path, "r") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    self._settings[key] = value

    def save_settings(self):
        with open(self._file_path, "w") as file:
            for key, value in self._settings.items():
                file.write(f"{key}={value}\n")

    def get_setting(self, key):
        return self._settings.get(key, None)

    def set_setting(self, key, value):
        self._settings[key] = value


class Report:
    def __init__(self):
        self.header = ""
        self.content = ""
        self.footer = ""

    def display(self):
        print("Header:", self.header)
        print("Content:", self.content)
        print("Footer:", self.footer)
        print()


class IReportBuilder(ABC):
    @abstractmethod
    def set_header(self, header): pass

    @abstractmethod
    def set_content(self, content): pass

    @abstractmethod
    def set_footer(self, footer): pass

    @abstractmethod
    def get_report(self): pass


class TextReportBuilder(IReportBuilder):
    def __init__(self):
        self.report = Report()

    def set_header(self, header):
        self.report.header = f"[TEXT] {header}"

    def set_content(self, content):
        self.report.content = content

    def set_footer(self, footer):
        self.report.footer = footer

    def get_report(self):
        return self.report


class HtmlReportBuilder(IReportBuilder):
    def __init__(self):
        self.report = Report()

    def set_header(self, header):
        self.report.header = f"<h1>{header}</h1>"

    def set_content(self, content):
        self.report.content = f"<p>{content}</p>"

    def set_footer(self, footer):
        self.report.footer = f"<footer>{footer}</footer>"

    def get_report(self):
        return self.report


class ReportDirector:
    def construct_report(self, builder, header, content, footer):
        builder.set_header(header)
        builder.set_content(content)
        builder.set_footer(footer)
        return builder.get_report()


class Discount:
    def __init__(self, name, percentage):
        self.name = name
        self.percentage = percentage

    def clone(self):
        return copy.deepcopy(self)


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def clone(self):
        return copy.deepcopy(self)


class Order:
    def __init__(self, customer_id, products, shipping_cost, discount):
        self.customer_id = customer_id
        self.products = products
        self.shipping_cost = shipping_cost
        self.discount = discount

    def calculate_total(self):
        total = sum(p.price * p.quantity for p in self.products)
        total -= total * self.discount.percentage
        total += self.shipping_cost
        return total

    def clone(self):
        return copy.deepcopy(self)


def run_tests():
    config1 = ConfigurationManager.get_instance()
    config2 = ConfigurationManager.get_instance()
    config1.set_setting("theme", "dark")
    assert config1 is config2

    director = ReportDirector()
    text_report = director.construct_report(TextReportBuilder(), "Q1 Report", "Sales up 20%", "End of Report")
    html_report = director.construct_report(HtmlReportBuilder(), "Q1 Report", "Sales up 20%", "End of Report")
    text_report.display()
    html_report.display()

    base_product = Product("Laptop", 1200, 1)
    base_discount = Discount("Standard", 0.10)
    base_order = Order(1, [base_product], 25, base_discount)

    new_order = base_order.clone()
    new_order.customer_id = 2
    new_order.products[0].price = 900
    new_order.discount.percentage = 0.20

    print("Base Order Total:", base_order.calculate_total())
    print("New Order Total:", new_order.calculate_total())


if __name__ == "__main__":
    run_tests()

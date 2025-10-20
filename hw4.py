from abc import ABC, abstractmethod

class IVehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

    @abstractmethod
    def refuel(self):
        pass


class Car(IVehicle):
    def __init__(self, make, model, fuel_type):
        self.make = make
        self.model = model
        self.fuel_type = fuel_type

    def drive(self):
        print(f"Car {self.make} {self.model} is driving.")

    def refuel(self):
        print(f"Car is refueling with {self.fuel_type}.")


class Motorcycle(IVehicle):
    def __init__(self, bike_type, engine_volume):
        self.bike_type = bike_type
        self.engine_volume = engine_volume

    def drive(self):
        print(f"{self.bike_type.capitalize()} motorcycle is moving at {self.engine_volume}cc.")

    def refuel(self):
        print("Motorcycle is refueling.")


class Truck(IVehicle):
    def __init__(self, load_capacity, axles):
        self.load_capacity = load_capacity
        self.axles = axles

    def drive(self):
        print(f"Truck with {self.axles} axles carrying {self.load_capacity} tons is on the move.")

    def refuel(self):
        print("Truck is refueling with diesel.")


class Bus(IVehicle):
    def __init__(self, capacity, route):
        self.capacity = capacity
        self.route = route

    def drive(self):
        print(f"Bus with capacity {self.capacity} is on route {self.route}.")

    def refuel(self):
        print("Bus is refueling.")


class ElectricScooter(IVehicle):
    def __init__(self, battery_level, range_km):
        self.battery_level = battery_level
        self.range_km = range_km

    def drive(self):
        print(f"Electric scooter is riding silently ({self.battery_level}% battery).")

    def refuel(self):
        print("Scooter is charging its battery.")


class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self, params: dict) -> IVehicle:
        pass


class CarFactory(VehicleFactory):
    def create_vehicle(self, params: dict) -> IVehicle:
        return Car(params['make'], params['model'], params['fuel'])


class MotorcycleFactory(VehicleFactory):
    def create_vehicle(self, params: dict) -> IVehicle:
        return Motorcycle(params['type'], params['volume'])


class TruckFactory(VehicleFactory):
    def create_vehicle(self, params: dict) -> IVehicle:
        return Truck(params['capacity'], params['axles'])


class BusFactory(VehicleFactory):
    def create_vehicle(self, params: dict) -> IVehicle:
        return Bus(params['capacity'], params['route'])


class ElectricScooterFactory(VehicleFactory):
    def create_vehicle(self, params: dict) -> IVehicle:
        return ElectricScooter(params['battery'], params['range'])


def get_factory(vehicle_type: str):
    factories = {
        'car': (CarFactory, ['make', 'model', 'fuel']),
        'motorcycle': (MotorcycleFactory, ['type', 'volume']),
        'truck': (TruckFactory, ['capacity', 'axles']),
        'bus': (BusFactory, ['capacity', 'route']),
        'scooter': (ElectricScooterFactory, ['battery', 'range'])
    }
    return factories.get(vehicle_type.lower())


def main():
    print("Vehicle types: Car, Motorcycle, Truck, Bus, Scooter")
    vehicle_type = input("Enter vehicle type: ").strip()
    factory_info = get_factory(vehicle_type)

    if not factory_info:
        print("Unknown vehicle type.")
        return

    factory_class, param_list = factory_info
    params = {}

    for param in param_list:
        params[param] = input(f"Enter {param}: ").strip()

    factory = factory_class()
    vehicle = factory.create_vehicle(params)
    vehicle.drive()
    vehicle.refuel()


if __name__ == "__main__":
    main()
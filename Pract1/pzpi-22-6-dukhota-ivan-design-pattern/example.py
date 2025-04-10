from abc import ABC, abstractmethod


# Абстрактні продукти
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

class Motorcycle(ABC):
    @abstractmethod
    def ride(self):
        pass


# Конкретні продукти для спортивних автомобілів та мотоциклів
class SportsCar(Car):
    def drive(self):
        return "Driving a sports car at high speed."
class SportsMotorcycle(Motorcycle):
    def ride(self):
        return "Riding a sports motorcycle at high speed."


# Конкретні продукти для класичних автомобілів та мотоциклів
class ClassicCar(Car):
    def drive(self):
        return "Driving a classic car leisurely."
class ClassicMotorcycle(Motorcycle):
    def ride(self):
        return "Riding a classic motorcycle leisurely."


# Абстрактна фабрика
class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass
    @abstractmethod
    def create_motorcycle(self):
        pass


# Конкретні фабрики для спортивних та класичних транспортних засобів
class SportsVehicleFactory(VehicleFactory):
    def create_car(self):
        return SportsCar()

    def create_motorcycle(self):
        return SportsMotorcycle()
class ClassicVehicleFactory(VehicleFactory):
    def create_car(self):
        return ClassicCar()

    def create_motorcycle(self):
        return ClassicMotorcycle()


# Клієнтський код
def vehicle_client(factory: VehicleFactory):
    car = factory.create_car()
    motorcycle = factory.create_motorcycle()

    print(car.drive())
    print(motorcycle.ride())


# Використання спортивної фабрики
print("Sports Vehicles:")
sports_factory = SportsVehicleFactory()
vehicle_client(sports_factory)

# Використання класичної фабрики
print("\nClassic Vehicles:")
classic_factory = ClassicVehicleFactory()
vehicle_client(classic_factory)


# =========================================================
# ЛАБОРАТОРНА РОБОТА №1
# Тема: Принципи SOLID у Python
# =========================================================


# =========================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =========================================================

print("\n====================")
print("1.1 SRP")
print("====================")


# Клас лише створює звіт
class ReportGenerator:
    def generate_report(self):
        print("Звіт про дзвінки сформовано")


# Клас лише зберігає звіт
class ReportSaver:
    def save_to_file(self):
        print("Звіт збережено у файл")


generator = ReportGenerator()
generator.generate_report()

saver = ReportSaver()
saver.save_to_file()


# ---------------------------------------------------------

print("\n====================")
print("1.2 SRP")
print("====================")


# Клас для даних абонента
class Subscriber:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


# Клас для SMS
class SMSService:
    def send_sms(self, phone, message):
        print(f"SMS на номер {phone}: {message}")


# Клас для балансу
class BalanceCalculator:
    def calculate_balance(self, balance, payment):
        return balance + payment


subscriber = Subscriber("Іван", "+380991112233")

sms_service = SMSService()
sms_service.send_sms(subscriber.phone, "Ваш баланс поповнено")

balance_service = BalanceCalculator()
new_balance = balance_service.calculate_balance(100, 50)

print("Новий баланс:", new_balance)


# =========================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# =========================================================

print("\n====================")
print("2.1 OCP")
print("====================")


# Базовий тариф
class Tariff:
    def calculate_price(self, minutes):
        pass


# Базовий тариф
class BasicTariff(Tariff):
    def calculate_price(self, minutes):
        return minutes * 1


# Новий тариф
class NightTariff(Tariff):
    def calculate_price(self, minutes):
        return minutes * 0.5


basic = BasicTariff()
night = NightTariff()

print("Basic tariff:", basic.calculate_price(10))
print("Night tariff:", night.calculate_price(10))


# ---------------------------------------------------------

print("\n====================")
print("2.2 OCP")
print("====================")


class TelecomTariff:
    def calculate(self, amount):
        pass


class VoiceTariff(TelecomTariff):
    def calculate(self, minutes):
        return minutes * 2


class DataTariff(TelecomTariff):
    def calculate(self, gb):
        return gb * 5


# Новий тариф без зміни старого коду
class RoamingTariff(TelecomTariff):
    def calculate(self, minutes):
        return minutes * 10


voice = VoiceTariff()
data = DataTariff()
roaming = RoamingTariff()

print("Voice tariff:", voice.calculate(20))
print("Data tariff:", data.calculate(5))
print("Roaming tariff:", roaming.calculate(15))


# =========================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# =========================================================

print("\n====================")
print("3.1 LSP")
print("====================")


class NetworkConnection:
    def connect(self):
        print("Підключення до мережі")


class LTEConnection(NetworkConnection):
    def connect(self):
        print("LTE підключено")


class WiFiConnection(NetworkConnection):
    def connect(self):
        print("WiFi підключено")


def start_connection(connection):
    connection.connect()


lte = LTEConnection()
wifi = WiFiConnection()

start_connection(lte)
start_connection(wifi)


# ---------------------------------------------------------

print("\n====================")
print("3.2 LSP")
print("====================")


# Правильна ієрархія


class Connection:
    def connect(self):
        print("З'єднання встановлено")


class StandardConnection(Connection):
    def connect(self):
        print("Стандартне з'єднання активне")


class SatelliteConnection(Connection):
    def connect(self):
        print("Супутникове з'єднання активне")


standard = StandardConnection()
satellite = SatelliteConnection()

standard.connect()
satellite.connect()


# =========================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# =========================================================

print("\n====================")
print("4.1 ISP")
print("====================")


# Інтерфейси


class Callable:
    def make_call(self):
        pass


class SMSable:
    def send_sms(self):
        pass


class InternetConnectable:
    def connect_to_network(self):
        pass


# Смартфон підтримує все
class Smartphone(Callable, SMSable, InternetConnectable):
    def make_call(self):
        print("Виконується дзвінок")

    def send_sms(self):
        print("SMS відправлено")

    def connect_to_network(self):
        print("Підключення до інтернету")


phone = Smartphone()

phone.make_call()
phone.send_sms()
phone.connect_to_network()


# ---------------------------------------------------------

print("\n====================")
print("4.2 ISP")
print("====================")


# Інтерфейс лише для передачі даних
class DataTransferable:
    def send_data(self):
        pass


# IoT-пристрій
class IoTDevice(DataTransferable):
    def send_data(self):
        print("IoT-пристрій передає дані")


iot = IoTDevice()
iot.send_data()


# =========================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# =========================================================

print("\n====================")
print("5.1 DIP")
print("====================")


# Абстракція логера
class Logger:
    def log(self, message):
        pass


# Реалізація логера
class FileLogger(Logger):
    def log(self, message):
        print("Запис у файл:", message)


# Система моніторингу
class NetworkMonitor:
    def __init__(self, logger):
        self.logger = logger

    def check_network(self):
        self.logger.log("Мережа працює стабільно")


file_logger = FileLogger()

monitor = NetworkMonitor(file_logger)
monitor.check_network()


# ---------------------------------------------------------

print("\n====================")
print("5.2 DIP")
print("====================")


class FileLogger(Logger):
    def log(self, message):
        print("Файл:", message)


class ServerLogger(Logger):
    def log(self, message):
        print("Сервер:", message)


class ConsoleLogger(Logger):
    def log(self, message):
        print("Консоль:", message)


class NetworkMonitor:
    def __init__(self, logger):
        self.logger = logger

    def check_network(self):
        self.logger.log("Перевірка мережі завершена")


file_logger = FileLogger()
server_logger = ServerLogger()
console_logger = ConsoleLogger()

monitor1 = NetworkMonitor(file_logger)
monitor2 = NetworkMonitor(server_logger)
monitor3 = NetworkMonitor(console_logger)

monitor1.check_network()
monitor2.check_network()
monitor3.check_network()
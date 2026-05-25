class MathTool:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Ділення на нуль неможливе")
        return a / b


class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def details(self):
        return f"Назва: {self.title}, Автор: {self.author}, Рік: {self.year}"


class NotificationService:
    def send(self, email, message):
        print(f"Повідомлення надіслано на {email}: {message}")


class UserManager:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def notify_user(self, email, message):
        self.notification_service.send(email, message)


def check_even(number):
    return number % 2 == 0


def main():
    math_tool = MathTool()

    print("Додавання:", math_tool.add(5, 3))
    print("Віднімання:", math_tool.subtract(5, 3))
    print("Множення:", math_tool.multiply(5, 3))
    print("Ділення:", math_tool.divide(10, 2))

    book = LibraryItem("Python для початківців", "Іван Петренко", 2023)
    print(book.details())

    service = NotificationService()
    manager = UserManager(service)
    manager.notify_user("student@gmail.com", "Тестове повідомлення")

    print("Число 4 парне:", check_even(4))


if __name__ == "__main__":
    main()
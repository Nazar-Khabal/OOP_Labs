import unittest
from unittest.mock import Mock
from parameterized import parameterized

from main import MathTool, LibraryItem, NotificationService, UserManager, check_even


class TestMathTool(unittest.TestCase):
    def setUp(self):
        self.math_tool = MathTool()

    def test_add(self):
        self.assertEqual(self.math_tool.add(5, 3), 8)

    def test_subtract(self):
        self.assertEqual(self.math_tool.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(self.math_tool.multiply(5, 3), 15)

    def test_divide(self):
        self.assertEqual(self.math_tool.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.math_tool.divide(10, 0)


class TestLibraryItem(unittest.TestCase):
    @parameterized.expand([
        ("Python", "Іван Петренко", 2023, "Назва: Python, Автор: Іван Петренко, Рік: 2023"),
        ("ООП", "Марія Коваль", 2022, "Назва: ООП, Автор: Марія Коваль, Рік: 2022"),
        ("Бази даних", "Олег Іванов", 2021, "Назва: Бази даних, Автор: Олег Іванов, Рік: 2021"),
    ])
    def test_details(self, title, author, year, expected):
        item = LibraryItem(title, author, year)
        self.assertEqual(item.details(), expected)


class TestUserManager(unittest.TestCase):
    def test_notify_user(self):
        mock_service = Mock(spec=NotificationService)

        manager = UserManager(mock_service)
        manager.notify_user("test@gmail.com", "Привіт!")

        mock_service.send.assert_called_once_with("test@gmail.com", "Привіт!")


class TestCheckEven(unittest.TestCase):
    @parameterized.expand([
        (2, True),
        (3, False),
        (0, True),
        (-4, True),
        (-7, False),
        (10, True),
        (15, False),
    ])
    def test_check_even(self, number, expected):
        self.assertEqual(check_even(number), expected)


if __name__ == "__main__":
    unittest.main()
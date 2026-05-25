import requests


class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        url = self.base_url + endpoint

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                print("Помилка GET-запиту:", response.status_code)
                return None

        except requests.exceptions.RequestException as error:
            print("Помилка підключення:", error)
            return None

    def post(self, endpoint, data):
        url = self.base_url + endpoint

        try:
            response = requests.post(url, json=data)

            if response.status_code == 201:
                return response.json()
            else:
                print("Помилка POST-запиту:", response.status_code)
                return None

        except requests.exceptions.RequestException as error:
            print("Помилка підключення:", error)
            return None


def main():
    client = RestClient("https://jsonplaceholder.typicode.com")

    print("GET-запит. Отримання перших 3 постів:")
    posts = client.get("/posts")

    if posts:
        for post in posts[:3]:
            print(f"ID: {post['id']}")
            print(f"Заголовок: {post['title']}")
            print(f"Текст: {post['body']}")
            print("-" * 30)

    print("\nPOST-запит. Створення нового поста:")

    new_post = {
        "title": "Лабораторна робота REST API",
        "body": "Це тестовий пост, створений через POST-запит.",
        "userId": 1
    }

    created_post = client.post("/posts", new_post)

    if created_post:
        print("Пост створено:")
        print("ID:", created_post["id"])
        print("Заголовок:", created_post["title"])
        print("Текст:", created_post["body"])
        print("User ID:", created_post["userId"])


main()
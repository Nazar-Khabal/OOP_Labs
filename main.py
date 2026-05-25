import asyncio
import ssl
import certifi
import websockets


class WebSocketClient:
    def __init__(self):
        self.connection = None

    async def connect(self, url):
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            self.connection = await websockets.connect(
                url,
                ssl=ssl_context
            )

            print("Підключення встановлено")
            return True

        except Exception as error:
            print("Помилка підключення:", error)
            return False

    async def send_message(self, message):
        if self.connection is None:
            print("Немає підключення до сервера")
            return

        try:
            await self.connection.send(message)
            print("Надіслано повідомлення:", message)

        except Exception as error:
            print("Помилка надсилання:", error)

    async def receive_message(self):
        if self.connection is None:
            print("Немає підключення до сервера")
            return

        try:
            response = await asyncio.wait_for(
                self.connection.recv(),
                timeout=5
            )

            print("Відповідь сервера:", response)
            return response

        except asyncio.TimeoutError:
            print("Сервер не відповідає")

        except Exception as error:
            print("Помилка отримання:", error)

    async def close_connection(self):
        if self.connection is None:
            print("З'єднання не було створено")
            return

        try:
            await self.connection.close()
            print("З'єднання закрито")

        except Exception as error:
            print("Помилка закриття:", error)


async def main():
    url = "wss://ws.postman-echo.com/raw"

    client = WebSocketClient()

    connected = await client.connect(url)

    if not connected:
        return

    await client.send_message("Привіт, сервер!")
    await client.receive_message()

    await client.send_message("Лабораторна робота 7 WebSocket")
    await client.receive_message()

    await client.close_connection()


asyncio.run(main())
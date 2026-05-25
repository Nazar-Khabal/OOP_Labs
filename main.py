import json
import time
import ssl
import certifi
import asyncio
import requests
import websockets
import paho.mqtt.client as mqtt


class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        try:
            response = requests.get(self.base_url + endpoint)

            if response.status_code == 200:
                return response.json()
            else:
                print("Помилка REST API:", response.status_code)
                return None

        except requests.exceptions.RequestException as error:
            print("Помилка REST підключення:", error)
            return None


class WebSocketClient:
    def __init__(self, url):
        self.url = url

    async def send_data(self, message):
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            async with websockets.connect(self.url, ssl=ssl_context) as websocket:
                await websocket.send(message)
                response = await websocket.recv()
                return response

        except Exception as error:
            print("Помилка WebSocket:", error)
            return None


class MQTTClient:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Підключено до MQTT брокера")
        else:
            print("Помилка MQTT підключення:", reason_code)

    def on_publish(self, client, userdata, mid, reason_code, properties):
        print("Повідомлення опубліковано")

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        print("Відключено від MQTT брокера")

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            time.sleep(1)

        except Exception as error:
            print("Помилка підключення до MQTT:", error)

    def publish(self, topic, message):
        try:
            result = self.client.publish(topic, message)
            result.wait_for_publish()
            print("Опубліковано в тему:", topic)

        except Exception as error:
            print("Помилка публікації MQTT:", error)

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()


async def main():
    rest_client = RestClient("https://jsonplaceholder.typicode.com")
    websocket_client = WebSocketClient("wss://ws.postman-echo.com/raw")
    mqtt_client = MQTTClient("broker.hivemq.com", 1883)

    print("Отримання даних через REST API...")
    post = rest_client.get("/posts/1")

    if post is None:
        return

    data = {
        "id": post["id"],
        "title": post["title"],
        "body": post["body"]
    }

    message = json.dumps(data, ensure_ascii=False)

    print("\nДані з REST API:")
    print(message)

    print("\nПередача даних через WebSocket...")
    websocket_response = await websocket_client.send_data(message)

    if websocket_response is None:
        return

    print("Відповідь WebSocket:")
    print(websocket_response)

    print("\nПублікація даних через MQTT...")
    mqtt_client.connect()
    mqtt_client.publish("oop/lab8/network_data", websocket_response)
    mqtt_client.disconnect()


asyncio.run(main())
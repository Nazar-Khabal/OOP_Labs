import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# =========================================================
# КЛАС ВУЗЛА
# =========================================================

class Node:

    def __init__(self, name):

        self.name = name
        self.connections = []

    # Підключення вузлів
    def connect(self, node):

        if node not in self.connections:

            self.connections.append(node)
            node.connections.append(self)

    # Відправка пакета
    async def send(self, packet, network):

        await asyncio.sleep(random.uniform(0.05, 0.3))

        # Втрата пакета
        if random.random() < network.loss_rate:

            print(f"[LOSS] {packet.src.name} -> {packet.dest.name}")

            network.packets_lost += 1
            return

        print(f"[SEND] {self.name}")

        await self.forward(packet, network)

    # Передача пакета далі
    async def forward(self, packet, network):

        # Якщо пакет доставлено
        if self == packet.dest:

            print(f"[DELIVERED] Пакет доставлено до {self.name}")
            return

        # Захист від циклів
        if self in packet.visited:
            return

        packet.visited.append(self)

        for node in self.connections:

            if node not in packet.visited:

                await node.send(packet, network)


# =========================================================
# МАРШРУТИЗАТОР
# =========================================================

class Router(Node):
    pass


# =========================================================
# КЛАС ПАКЕТА
# =========================================================

class Packet:

    def __init__(self, src, dest, size, protocol):

        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []


# =========================================================
# TCP ПРОТОКОЛ
# =========================================================

class TCPProtocol:

    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):

        packet = Packet(
            src,
            dest,
            random.randint(200, 500),
            "TCP"
        )

        print(f"\n[TCP] {src.name} -> {dest.name}")

        await src.send(packet, network)


# =========================================================
# UDP ПРОТОКОЛ
# =========================================================

class UDPProtocol:

    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):

        packet = Packet(
            src,
            dest,
            random.randint(50, 200),
            "UDP"
        )

        print(f"\n[UDP] {src.name} -> {dest.name}")

        await src.send(packet, network)


# =========================================================
# КЛАС МЕРЕЖІ
# =========================================================

class Network:

    def __init__(self, topology_name):

        self.topology_name = topology_name

        self.nodes = []

        self.loss_rate = random.uniform(0.10, 0.15)

        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    # Симуляція
    async def simulate(self, protocol, packets=5):

        print("\n====================================")
        print(f"ТОПОЛОГІЯ: {self.topology_name}")
        print(f"ПРОТОКОЛ: {protocol.name}")
        print("====================================")

        for _ in range(packets):

            src, dest = random.sample(self.nodes, 2)

            start_time = time.time()

            self.packets_sent += 1

            await protocol.transmit(src, dest, self)

            end_time = time.time()

            self.total_time += end_time - start_time

    # Аналіз
    def analyze(self):

        successful = self.packets_sent - self.packets_lost

        avg_time = self.total_time / self.packets_sent

        loss_percent = (
            self.packets_lost / self.packets_sent
        ) * 100

        bandwidth = successful / self.total_time

        print("\n========== АНАЛІЗ ==========")

        print(f"Передано пакетів: {self.packets_sent}")

        print(f"Втрачено пакетів: {self.packets_lost}")

        print(f"Втрати: {loss_percent:.2f}%")

        print(f"Середній час: {avg_time:.4f} с")

        print(f"Пропускна здатність: {bandwidth:.2f} пак/с")

    # Візуалізація
    def visualize(self):

        G = nx.Graph()

        for node in self.nodes:

            for conn in node.connections:

                G.add_edge(node.name, conn.name)

        plt.figure(figsize=(8, 6))

        pos = nx.spring_layout(G)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=3000,
            font_size=10,
            font_weight="bold",
            edge_color="gray"
        )

        plt.title(f"{self.topology_name} Topology")

        plt.show()


# =========================================================
# STAR TOPOLOGY
# =========================================================

def create_star_topology():

    network = Network("STAR")

    router = Router("Router")

    pcs = [
        Node("PC1"),
        Node("PC2"),
        Node("PC3"),
        Node("PC4"),
        Node("PC5")
    ]

    network.nodes = [router] + pcs

    for pc in pcs:
        router.connect(pc)

    return network


# =========================================================
# RING TOPOLOGY
# =========================================================

def create_ring_topology():

    network = Network("RING")

    nodes = [
        Node("PC1"),
        Node("PC2"),
        Node("PC3"),
        Node("PC4"),
        Node("PC5"),
        Node("PC6")
    ]

    network.nodes = nodes

    for i in range(len(nodes)):

        nodes[i].connect(
            nodes[(i + 1) % len(nodes)]
        )

    return network


# =========================================================
# MAIN
# =========================================================

async def main():

    # STAR TOPOLOGY

    star_network = create_star_topology()

    await star_network.simulate(
        TCPProtocol,
        packets=7
    )

    star_network.analyze()

    star_network.visualize()

    # RING TOPOLOGY

    ring_network = create_ring_topology()

    await ring_network.simulate(
        UDPProtocol,
        packets=7
    )

    ring_network.analyze()

    ring_network.visualize()


# =========================================================
# ЗАПУСК
# =========================================================

asyncio.run(main())
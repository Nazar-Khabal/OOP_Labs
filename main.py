import asyncio
from pathlib import Path

from sqlalchemy import Column, Integer, String, select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


# Шлях до папки, де лежить main.py
BASE_DIR = Path(__file__).parent

# База даних буде створена саме в Lab_5
DB_PATH = BASE_DIR / "network.db"

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    status = Column(String, default="unknown")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_nodes():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM nodes"))
        await session.commit()


async def add_nodes():
    async with AsyncSessionLocal() as session:
        nodes = []

        for i in range(1, 13):
            node = Node(
                ip_address=f"192.168.1.{i}",
                status="unknown"
            )
            nodes.append(node)

        session.add_all(nodes)
        await session.commit()


async def get_nodes(title):
    print(f"\n{title}")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()

        for node in nodes:
            print(f"ID: {node.id}, IP: {node.ip_address}, Status: {node.status}")


async def check_node_status(ip_address):
    await asyncio.sleep(0.3)

    last_number = int(ip_address.split(".")[-1])

    if last_number % 2 == 0:
        return "offline"
    else:
        return "active"


async def update_node_status(node_id, ip_address):
    new_status = await check_node_status(ip_address)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Node).where(Node.id == node_id)
        )

        node = result.scalar_one()
        node.status = new_status

        await session.commit()


async def monitor_nodes():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()

    tasks = []

    for node in nodes:
        task = update_node_status(node.id, node.ip_address)
        tasks.append(task)

    await asyncio.gather(*tasks)


async def main():
    print(f"База даних зберігається тут: {DB_PATH}")

    await create_tables()
    await reset_nodes()
    await add_nodes()

    await get_nodes("Список вузлів до моніторингу:")

    await monitor_nodes()

    await get_nodes("Список вузлів після моніторингу:")


asyncio.run(main())
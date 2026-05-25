from pathlib import Path
import pandas as pd


class NetworkData:
    def __init__(self):
        self.data = {
            "node": ["Router_1", "Router_2", "Switch_1", "Switch_2", "Server_1"],
            "protocol": ["TCP", "UDP", "TCP", "UDP", "TCP"],
            "packets": [1200, 950, 1500, 700, 2000],
            "packet_size_kb": [64, 32, 64, 16, 128],
            "delay_ms": [12, 8, 15, 6, 20]
        }

    def create_dataframe(self):
        return pd.DataFrame(self.data)


class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def add_columns(self):
        self.df["traffic_mb"] = self.df["packets"] * self.df["packet_size_kb"] / 1024

        self.df["status"] = self.df["delay_ms"].apply(
            lambda x: "нормальна" if x <= 10 else "велика"
        )

    def show_info(self):
        print("Перші 5 рядків:")
        print(self.df.head())

        print("\nРозмір таблиці:")
        print(self.df.shape)

        print("\nТипи даних:")
        print(self.df.dtypes)

    def filter_data(self):
        print("\nВузли з великою затримкою:")
        print(self.df[self.df["delay_ms"] > 10])

    def sort_data(self):
        print("\nСортування за трафіком:")
        print(self.df.sort_values(by="traffic_mb", ascending=False))

    def group_data(self):
        print("\nГрупування за протоколом:")
        print(self.df.groupby("protocol").agg({
            "packets": "sum",
            "traffic_mb": "sum",
            "delay_ms": "mean"
        }))


def main():
    folder = Path(__file__).parent
    file_path = folder / "network_data.csv"

    network_data = NetworkData()
    df = network_data.create_dataframe()

    df.to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    analyzer = DataAnalyzer(df)
    analyzer.add_columns()
    analyzer.show_info()
    analyzer.filter_data()
    analyzer.sort_data()
    analyzer.group_data()

    df.to_csv(file_path, index=False)

    print(f"\nФайл збережено: {file_path}")


if __name__ == "__main__":
    main()
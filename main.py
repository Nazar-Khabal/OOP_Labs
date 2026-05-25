from pathlib import Path
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "Job opportunities.csv"


class DataLoader:
    def load_data(self):
        if CSV_FILE.exists():
            df = pd.read_csv(CSV_FILE)
            print("Завантажено файл Job opportunities.csv")
        else:
            print("Файл не знайдено, використано тестові дані")
            df = pd.DataFrame({
                "Job Title": ["Python Developer", "Data Analyst", "DevOps Engineer", "QA Tester", "Backend Developer",
                              "Frontend Developer", "Data Scientist", "System Admin", "AI Engineer", "Web Developer"],
                "Salary Range": ["50000-70000", "60000-80000", "80000-110000", "40000-60000", "70000-95000",
                                 "55000-75000", "90000-130000", "45000-65000", "100000-150000", "50000-72000"],
                "Experience Level": ["Junior", "Middle", "Senior", "Junior", "Middle",
                                     "Junior", "Senior", "Middle", "Senior", "Junior"],
                "Industry": ["Software", "Analytics", "Cloud", "Software", "Software",
                             "Web", "AI", "IT Support", "AI", "Web"],
                "Date Posted": ["2019-05-12", "2020-06-20", "2021-03-15", "2019-11-10", "2022-07-01",
                                "2020-09-14", "2023-01-22", "2021-12-05", "2023-04-18", "2022-10-30"]
            })

        return df


class DataProcessor:
    def get_average_salary(self, salary):
        numbers = re.findall(r"\d+", str(salary))
        numbers = [int(num) for num in numbers]

        if len(numbers) >= 2:
            return sum(numbers[:2]) / 2
        elif len(numbers) == 1:
            return numbers[0]
        else:
            return 0

    def prepare_data(self, df):
        df["Average Salary"] = df["Salary Range"].apply(self.get_average_salary)
        df["Date Posted"] = pd.to_datetime(df["Date Posted"])
        df["Year"] = df["Date Posted"].dt.year

        experience_map = {
            "Junior": 1,
            "Middle": 2,
            "Senior": 3,
            "Entry": 1,
            "Mid": 2,
            "Lead": 4
        }

        df["Experience Code"] = df["Experience Level"].map(experience_map)
        df["Experience Code"] = df["Experience Code"].fillna(0)

        return df


class DataVisualizer:
    def barplot_salary_by_experience(self, df):
        plt.figure(figsize=(8, 5))
        sns.barplot(x="Experience Level", y="Average Salary", data=df)
        plt.title("Середня зарплата за рівнем досвіду")
        plt.xlabel("Рівень досвіду")
        plt.ylabel("Середня зарплата")
        plt.tight_layout()
        plt.savefig(BASE_DIR / "barplot_salary_experience.png")
        plt.show()

    def boxplot_salary_by_industry(self, df):
        plt.figure(figsize=(12, 6))
        sns.boxplot(x="Industry", y="Average Salary", data=df)
        plt.title("Розподіл зарплат за галузями")
        plt.xlabel("Галузь")
        plt.ylabel("Середня зарплата")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(BASE_DIR / "boxplot_salary_industry.png")
        plt.show()

    def heatmap_jobs(self, df):
        pivot_table = pd.crosstab(df["Experience Level"], df["Industry"])

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, fmt="d")
        plt.title("Кількість вакансій за досвідом та галуззю")
        plt.xlabel("Галузь")
        plt.ylabel("Рівень досвіду")
        plt.tight_layout()
        plt.savefig(BASE_DIR / "heatmap_jobs.png")
        plt.show()

    def scatterplot_salary_by_year(self, df):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="Year",
            y="Average Salary",
            hue="Experience Level",
            data=df
        )
        plt.title("Залежність зарплати від року")
        plt.xlabel("Рік")
        plt.ylabel("Середня зарплата")
        plt.tight_layout()
        plt.savefig(BASE_DIR / "scatterplot_salary_year.png")
        plt.show()

    def pairplot_data(self, df):
        sns.pairplot(
            df,
            vars=["Average Salary", "Year", "Experience Code"],
            hue="Experience Level"
        )
        plt.suptitle("Парні графіки для зарплати, року та досвіду", y=1.02)
        plt.savefig(BASE_DIR / "pairplot_data.png")
        plt.show()


def main():
    loader = DataLoader()
    processor = DataProcessor()
    visualizer = DataVisualizer()

    df = loader.load_data()
    df = processor.prepare_data(df)

    print("\nПерші 5 рядків таблиці:")
    print(df.head())

    print("\nСередня зарплата за рівнем досвіду:")
    print(df.groupby("Experience Level")["Average Salary"].mean())

    print("\nКількість вакансій за галузями:")
    print(df["Industry"].value_counts())

    visualizer.barplot_salary_by_experience(df)
    visualizer.boxplot_salary_by_industry(df)
    visualizer.heatmap_jobs(df)
    visualizer.scatterplot_salary_by_year(df)
    visualizer.pairplot_data(df)

    print("\nВисновок:")
    print("Було виконано візуалізацію даних про IT-вакансії за допомогою Seaborn.")
    print("Найвища середня зарплата зазвичай спостерігається у вакансіях з більшим рівнем досвіду.")
    print("Heatmap показує кількість вакансій за галузями та рівнями досвіду.")
    print("Scatterplot і pairplot допомагають побачити залежність зарплати від року та досвіду.")


main()
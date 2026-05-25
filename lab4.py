import sqlite3
import pandas as pd
import re
from pathlib import Path


class DataLoader:
    def __init__(self, csv_name):
        self.csv_path = Path(__file__).resolve().parent / csv_name

    def create_test_csv(self):
        data = [
            ["Python Developer", "SoftServe", "Lviv", "Junior", "£30000 - £45000", "Python, SQL, Git", "Software Development", "Full-time", 2023, "Remote"],
            ["Data Analyst", "EPAM", "Kyiv", "Middle", "£50000 - £70000", "SQL, Pandas, Excel", "Data", "Full-time", 2023, "Hybrid"],
            ["Backend Developer", "GlobalLogic", "Lviv", "Middle", "£55000 - £80000", "Python, SQL, Django", "Software Development", "Full-time", 2022, "Office"],
            ["QA Engineer", "N-iX", "Kyiv", "Junior", "£28000 - £40000", "Testing, SQL, Jira", "Quality Assurance", "Part-time", 2021, "Remote"],
            ["DevOps Engineer", "Intellias", "Odesa", "Senior", "£80000 - £110000", "Linux, Docker, AWS", "Infrastructure", "Full-time", 2023, "Remote"],
            ["Frontend Developer", "Luxoft", "Kharkiv", "Junior", "£35000 - £50000", "JavaScript, React, HTML", "Software Development", "Full-time", 2020, "Hybrid"],
            ["Database Admin", "ELEKS", "Lviv", "Senior", "£75000 - £100000", "SQL, PostgreSQL, Linux", "Data", "Contract", 2023, "Office"],
            ["Project Manager", "Sigma Software", "Kyiv", "Senior", "£70000 - £95000", "Scrum, Jira, Communication", "Management", "Full-time", 2022, "Hybrid"],
            ["ML Engineer", "Ciklum", "Dnipro", "Middle", "£65000 - £90000", "Python, SQL, Machine Learning", "AI", "Full-time", 2023, "Remote"],
            ["Support Engineer", "Infopulse", "Odesa", "Junior", "£25000 - £35000", "Support, Linux, SQL", "Support", "Part-time", 2019, "Office"],
            ["Security Analyst", "SoftServe", "Lviv", "Middle", "£60000 - £85000", "Security, SQL, Python", "Cybersecurity", "Full-time", 2023, "Hybrid"],
            ["Business Analyst", "EPAM", "Kyiv", "Middle", "£52000 - £72000", "SQL, UML, Communication", "Business Analysis", "Contract", 2021, "Remote"]
        ]

        columns = [
            "Job Title", "Company", "Location", "Experience Level", "Salary Range",
            "Required Skills", "Industry", "Job Type", "Year", "Work Mode"
        ]

        df = pd.DataFrame(data, columns=columns)
        df.to_csv(self.csv_path, index=False)

    def salary_numbers(self, value):
        numbers = re.findall(r"\d+", str(value).replace(",", ""))
        numbers = [int(num) for num in numbers]
        numbers = [num * 1000 if num < 1000 else num for num in numbers]
        return numbers

    def load_data(self):
        if not self.csv_path.exists():
            self.create_test_csv()

        df = pd.read_csv(self.csv_path)

        df["Min Salary"] = df["Salary Range"].apply(lambda x: self.salary_numbers(x)[0])
        df["Max Salary"] = df["Salary Range"].apply(lambda x: self.salary_numbers(x)[1])
        df["Avg Salary"] = (df["Min Salary"] + df["Max Salary"]) / 2

        return df


class JobDatabase:
    def __init__(self, db_name):
        self.db_path = Path(__file__).resolve().parent / db_name
        self.conn = sqlite3.connect(self.db_path)

    def save_to_db(self, df):
        df.to_sql("jobs", self.conn, if_exists="replace", index=False)

    def query(self, title, sql):
        print("\n" + title)
        result = pd.read_sql_query(sql, self.conn)
        print(result)

    def close(self):
        self.conn.close()


class JobAnalyzer:
    def __init__(self, database):
        self.database = database

    def show_main_queries(self):
        self.database.query(
            "1. Перші 10 вакансій:",
            "SELECT * FROM jobs LIMIT 10"
        )

        self.database.query(
            "2. Вакансії, де потрібен SQL:",
            "SELECT * FROM jobs WHERE `Required Skills` LIKE '%SQL%'"
        )

        self.database.query(
            "3. Унікальні локації:",
            "SELECT DISTINCT Location FROM jobs"
        )

        self.database.query(
            "4. Унікальні компанії:",
            "SELECT DISTINCT Company FROM jobs"
        )

    def show_analytics(self):
        self.database.query(
            "5. Середня зарплата для кожного рівня досвіду:",
            """
            SELECT `Experience Level`, ROUND(AVG(`Avg Salary`), 2) AS avg_salary
            FROM jobs
            GROUP BY `Experience Level`
            """
        )

        self.database.query(
            "6. Кількість вакансій для кожного рівня досвіду:",
            """
            SELECT `Experience Level`, COUNT(*) AS count_jobs
            FROM jobs
            GROUP BY `Experience Level`
            """
        )

        self.database.query(
            "7. Мінімальна та максимальна зарплата:",
            """
            SELECT MIN(`Min Salary`) AS min_salary, MAX(`Max Salary`) AS max_salary
            FROM jobs
            """
        )

        self.database.query(
            "8. Кількість вакансій в індустріях із зарплатою більше 50000:",
            """
            SELECT Industry, COUNT(*) AS count_jobs
            FROM jobs
            WHERE `Avg Salary` > 50000
            GROUP BY Industry
            """
        )

        self.database.query(
            "9. Середня зарплата для кожної індустрії:",
            """
            SELECT Industry, ROUND(AVG(`Avg Salary`), 2) AS avg_salary
            FROM jobs
            GROUP BY Industry
            """
        )

    def show_hard_queries(self):
        self.database.query(
            "10. Кількість вакансій за Location та Experience Level:",
            """
            SELECT Location, `Experience Level`, COUNT(*) AS count_jobs
            FROM jobs
            GROUP BY Location, `Experience Level`
            """
        )

        self.database.query(
            "11. Кількість вакансій за Industry та Job Type:",
            """
            SELECT Industry, `Job Type`, COUNT(*) AS count_jobs
            FROM jobs
            GROUP BY Industry, `Job Type`
            """
        )

        self.database.query(
            "12. Середня зарплата за Location та Experience Level:",
            """
            SELECT Location, `Experience Level`, ROUND(AVG(`Avg Salary`), 2) AS avg_salary
            FROM jobs
            GROUP BY Location, `Experience Level`
            """
        )

        self.database.query(
            "13. 5 вакансій з найвищою верхньою межею зарплати:",
            """
            SELECT `Job Title`, Company, Location, `Max Salary`
            FROM jobs
            ORDER BY `Max Salary` DESC
            LIMIT 5
            """
        )

        self.database.query(
            "14. Компанії з найбільшою кількістю вакансій у 2023 році:",
            """
            SELECT Company, COUNT(*) AS count_jobs
            FROM jobs
            WHERE Year = 2023
            GROUP BY Company
            ORDER BY count_jobs DESC
            """
        )

    def show_skills_count(self, df):
        print("\n15. Кількість вакансій для кожної навички:")
        skills = df["Required Skills"].str.split(", ").explode()
        print(skills.value_counts())


def main():
    loader = DataLoader("Job opportunities.csv")
    df = loader.load_data()

    db = JobDatabase("jobs.db")
    db.save_to_db(df)

    analyzer = JobAnalyzer(db)
    analyzer.show_main_queries()
    analyzer.show_analytics()
    analyzer.show_hard_queries()
    analyzer.show_skills_count(df)

    db.close()
    print("\nВисновок: у лабораторній роботі було створено базу SQLite, завантажено дані з CSV та виконано SQL-запити для аналізу вакансій.")


if __name__ == "__main__":
    main()
import random
import csv
from faker import Faker
from datetime import datetime

fake = Faker()

TOTAL = 100_000
OUTPUT_FILE = "issues_seed_data.csv"

def generate_issues():
    with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["set_id", "user_id", "description", "created_at"])

        for _ in range(TOTAL):
            user_id = random.randint(1, 50000)
            set_id = random.randint(1, 20596)
            description = fake.sentence(nb_words=10)
            created_at = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            writer.writerow([set_id, user_id, description, created_at])

if __name__ == "__main__":
    generate_issues()
import random
import csv
from faker import Faker
from datetime import datetime

fake = Faker()
statuses = ["wishlist", "purchased", "building", "built"]

TOTAL = 500_000
OUTPUT_FILE = "lists_seed_data.csv"

def generate_list_entries():
    with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user_id", "set_id", "status", "created_at"])  

        for _ in range(TOTAL):
            user_id = random.randint(1, 50000)
            set_id = random.randint(1, 20596)
            status = random.choice(statuses)
            created_at = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            writer.writerow([user_id, set_id, status, created_at])

if __name__ == "__main__":
    generate_list_entries()
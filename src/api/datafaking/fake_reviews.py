import random
import csv
from faker import Faker
from datetime import datetime

fake = Faker()

TOTAL = 150_000
OUTPUT_FILE = "reviews_seed_data.csv"

def generate_reviews():
    with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["set_id", "user_id", "rating", "description", "created_at"])

        for _ in range(TOTAL):
            user_id = random.randint(1, 50000)
            set_id = random.randint(1, 20596)
            rating = random.randint(1, 5)
            description = fake.sentence(nb_words=8)
            created_at = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            writer.writerow([user_id, set_id, rating, description, created_at])

if __name__ == "__main__":
    generate_reviews()
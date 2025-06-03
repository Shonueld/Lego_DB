import random
import csv
from faker import Faker
from datetime import datetime

fake = Faker()

TOTAL = 100_000
OUTPUT_FILE = "issues_seed_data.csv"
LISTS_FILE = "lists_seed_data.csv" 

def load_built_pairs():
    built_pairs = []
    with open(LISTS_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "built":
                built_pairs.append((int(row["user_id"]), int(row["set_id"])))
    return built_pairs

def generate_issues(built_pairs):
    with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["set_id", "user_id", "description", "created_at"])

        chosen_pairs = random.sample(built_pairs, TOTAL)
        for user_id, set_id in chosen_pairs:
            description = fake.sentence(nb_words=10)
            created_at = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
            writer.writerow([set_id, user_id, description, created_at])

if __name__ == "__main__":
    built_pairs = load_built_pairs()
    if len(built_pairs) < TOTAL:
        raise Exception(f"Only {len(built_pairs)} built pairs available, need {TOTAL}")
    generate_issues(built_pairs)
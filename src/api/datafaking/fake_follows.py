import random
import csv
from faker import Faker
from datetime import datetime

fake = Faker()

TOTAL_USERS = 50000
FOLLOWS_PER_USER = 4
FOLLOW_OUTPUT = "followers_seed_data.csv"
LOG_OUTPUT = "follow_log_seed_data.csv"

def generate_follow_data():
    follows = set()

    with open(FOLLOW_OUTPUT, mode="w", newline="") as follow_csv, \
         open(LOG_OUTPUT, mode="w", newline="") as log_csv:

        follow_writer = csv.writer(follow_csv)
        follow_writer.writerow(["user_id", "following_id", "created_at"])

        log_writer = csv.writer(log_csv)
        log_writer.writerow(["user_id", "following_id", "status", "followed_at"])

        for user_id in range(1, TOTAL_USERS + 1):
            following_ids = set()
            while len(following_ids) < FOLLOWS_PER_USER:
                follow_id = random.randint(1, TOTAL_USERS)
                if follow_id != user_id and (user_id, follow_id) not in follows:
                    following_ids.add(follow_id)
                    follows.add((user_id, follow_id))

            for follow_id in following_ids:
                timestamp = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
                follow_writer.writerow([user_id, follow_id, timestamp])
                log_writer.writerow([user_id, follow_id, "followed", timestamp])

if __name__ == "__main__":
    generate_follow_data()
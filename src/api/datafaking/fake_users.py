import csv
from faker import Faker
from datetime import datetime
import random

faker = Faker()
output_file = "users.csv"
num_users = 50000

with open(output_file, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["user_id", "username", "created_at"])

    for user_id in range(1, num_users + 1):
        username = faker.unique.user_name()
        created_at = faker.date_time_between(start_date='-3y', end_date='now').isoformat()
        writer.writerow([user_id, username, created_at])

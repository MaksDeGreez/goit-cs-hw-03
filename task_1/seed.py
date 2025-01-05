# -*- coding: utf-8 -*-

import os
import psycopg2
from faker import Faker
import random

def seed_data():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()

    #
    # seed `status`
    #

    status_list = ["new", "in progress", "completed"]
    for s in status_list:
        cursor.execute(
            "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
            (s,)
        )

    #
    # seed `users`
    #

    fake = Faker()
    users_count = 10
    for _ in range(users_count):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;",
            (fullname, email)
        )
        user_id = cursor.fetchone()[0]

        #
        # seed `tasks`
        #

        tasks_for_user = random.randint(1, 4)
        for _t in range(tasks_for_user):
            title = fake.sentence(nb_words=4)
            description = fake.text(max_nb_chars=80)
            chosen_status = random.choice(status_list)
            cursor.execute("SELECT id FROM status WHERE name = %s;", (chosen_status,))
            status_id = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO tasks (title, description, status_id, user_id)
                   VALUES (%s, %s, %s, %s);""",
                (title, description, status_id, user_id)
            )

    conn.commit()
    cursor.close()
    conn.close()

    print("Tables are successfully seeded.")


if __name__ == "__main__":
    seed_data()

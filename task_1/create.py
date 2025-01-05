# -*- coding: utf-8 -*-

import os
import psycopg2

def create_tables():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()

    #
    # drop existing tables
    #

    drop_tasks = "DROP TABLE IF EXISTS tasks CASCADE;"
    drop_status = "DROP TABLE IF EXISTS status CASCADE;"
    drop_users = "DROP TABLE IF EXISTS users CASCADE;"

    cursor.execute(drop_tasks)
    cursor.execute(drop_status)
    cursor.execute(drop_users)

    #
    # create `users`
    #

    create_users = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """
    cursor.execute(create_users)

    #
    # create `status`
    #

    create_status = """
    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """
    cursor.execute(create_status)

    #
    # create `tasks`
    #

    create_tasks = """
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        CONSTRAINT fk_status
            FOREIGN KEY (status_id)
            REFERENCES status (id)
            ON DELETE RESTRICT,
        CONSTRAINT fk_user
            FOREIGN KEY (user_id)
            REFERENCES users (id)
            ON DELETE CASCADE
    );
    """
    cursor.execute(create_tasks)

    conn.commit()
    cursor.close()
    conn.close()

    print("All needed tables have been (re-)created")


if __name__ == "__main__":
    create_tables()

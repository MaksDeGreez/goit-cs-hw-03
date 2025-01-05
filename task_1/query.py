# -*- coding: utf-8 -*-

import os
import psycopg2

def run_queries():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()

    print("=== 1) Отримати всі завдання певного користувача (user_id=1) ===")
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (1,))
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 2) Вибрати завдання за певним статусом ('new') ===")
    cursor.execute("SELECT id FROM status WHERE name = %s;", ('new',))
    new_status_id = cursor.fetchone()
    if new_status_id:
        new_status_id = new_status_id[0]
        cursor.execute("SELECT * FROM tasks WHERE status_id = %s;", (new_status_id,))
        rows = cursor.fetchall()
        for r in rows:
            print(r)
    print()

    print("=== 3) Оновити статус конкретного завдання (id=1) на 'in progress' ===")
    cursor.execute("SELECT id FROM status WHERE name = %s;", ('in progress',))
    in_progress_id = cursor.fetchone()
    if in_progress_id:
        in_progress_id = in_progress_id[0]
        cursor.execute("UPDATE tasks SET status_id = %s WHERE id = %s;", (in_progress_id, 1))
        conn.commit()
        print("Завдання з id=1 оновлено до статусу 'in progress'")
    print()

    print("=== 4) Отримати список користувачів, які не мають жодного завдання ===")
    cursor.execute("DELETE FROM tasks WHERE user_id = (SELECT id FROM users ORDER BY id DESC LIMIT 1);")
    query_no_tasks = """
    SELECT * FROM users
    WHERE id NOT IN (SELECT user_id FROM tasks);
    """
    cursor.execute(query_no_tasks)
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 5) Додати нове завдання для конкретного користувача (user_id=1) ===")
    cursor.execute("SELECT id FROM status WHERE name = %s;", ('new',))
    new_status_id = cursor.fetchone()[0]

    cursor.execute(
        """INSERT INTO tasks (title, description, status_id, user_id)
           VALUES (%s, %s, %s, %s) RETURNING id;""",
        ("Нове завдання", "Це опис нового завдання", new_status_id, 1)
    )
    new_task_id = cursor.fetchone()[0]
    conn.commit()
    print(f"Додано нове завдання з id={new_task_id} для user_id=1\n")

    print("=== 6) Отримати всі завдання, які ще не завершено (статус != 'completed') ===")
    cursor.execute("SELECT id FROM status WHERE name = %s;", ('completed',))
    completed_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM tasks WHERE status_id != %s;", (completed_id,))
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 7) Видалити конкретне завдання (id=2) ===")
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (2,))
    conn.commit()
    print("Якщо завдання з id=2 існувало, то воно видалене.\n")

    print("=== 8) Знайти користувачів із певною електронною поштою (LIKE '%example.com%') ===")
    cursor.execute("SELECT * FROM users WHERE email LIKE %s;", ('%example.com%',))
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 9) Оновити ім'я користувача (id=1) ===")
    cursor.execute(
        "UPDATE users SET fullname = %s WHERE id = %s;",
        ("Нове Ім'я Користувача", 1)
    )
    conn.commit()
    print("fullname користувача з id=1 оновлено.\n")

    print("=== 10) Отримати кількість завдань для кожного статусу (COUNT, GROUP BY) ===")
    query_count_by_status = """
    SELECT s.name, COUNT(t.id)
    FROM status s
    LEFT JOIN tasks t ON t.status_id = s.id
    GROUP BY s.name;
    """
    cursor.execute(query_count_by_status)
    rows = cursor.fetchall()
    for r in rows:
        print(f"Статус: {r[0]}, кількість завдань: {r[1]}")
    print()

    print("=== 11) Отримати завдання, які призначені користувачам із доменом електронки '%@example.com' ===")
    query_tasks_domain = """
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s;
    """
    cursor.execute(query_tasks_domain, ('%@example.com',))
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 12) Отримати список завдань, що не мають опису (description IS NULL або '') ===")
    cursor.execute("UPDATE tasks SET description = '' WHERE id = (SELECT id FROM tasks ORDER BY id DESC LIMIT 1)")
    query_no_description = """
    SELECT * FROM tasks
    WHERE description IS NULL
       OR description = '';
    """
    cursor.execute(query_no_description)
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 13) Вибрати користувачів та їхні завдання, які є у статусі 'in progress' (INNER JOIN) ===")
    query_users_in_progress = """
    SELECT u.id, u.fullname, t.id, t.title
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    INNER JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress';
    """
    cursor.execute(query_users_in_progress)
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    print("=== 14) Отримати користувачів та кількість їхніх завдань (LEFT JOIN + GROUP BY) ===")
    query_users_task_count = """
    SELECT u.id, u.fullname, COUNT(t.id) AS task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id, u.fullname
    ORDER BY task_count DESC;
    """
    cursor.execute(query_users_task_count)
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print()

    cursor.close()
    conn.close()
    print("All queries run successfully.")


if __name__ == "__main__":
    run_queries()

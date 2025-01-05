# -*- coding: utf-8 -*-
import os
import pymongo
from bson.objectid import ObjectId
import re

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = "test_db"
COLLECTION_NAME = "cats"

def clear_input(s: str) -> str:
    return re.sub(r'[\ud800-\udfff]', '', s)

def show_all(cats_collection):
    print("=== Усі записи в колекції ===")
    all_cats = list(cats_collection.find({}))
    if not all_cats:
        print("Колекція порожня.")
        return
    for cat in all_cats:
        print(f"_id: {cat['_id']}, name: {cat['name']}, age: {cat['age']}, features: {cat['features']}")


def show_one_by_name(cats_collection):
    name = clear_input(input("Введіть ім'я кота для пошуку: ").strip())
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(f"Знайдено кота: {cat}")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


def update_age_by_name(cats_collection):
    name = clear_input(input("Введіть ім'я кота, вік якого хочете оновити: ").strip())
    new_age_str = input("Введіть новий вік: ").strip()
    try:
        new_age = int(new_age_str)
    except ValueError:
        print("Помилка: вік має бути цілим числом.")
        return

    result = cats_collection.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )
    if result.matched_count > 0:
        print(f"Вік кота '{name}' успішно оновлено до {new_age}.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


def add_feature_by_name(cats_collection):
    name = clear_input(input("Введіть ім'я кота, якому додаємо характеристику: ").strip())
    new_feature = input("Введіть назву нової характеристики: ").strip()

    result = cats_collection.update_one(
        {"name": name},
        {"$push": {"features": new_feature}}
    )
    if result.matched_count > 0:
        print(f"Характеристику '{new_feature}' додано коту з ім'ям '{name}'.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


def delete_one_by_name(cats_collection):
    name = clear_input(input("Введіть ім'я кота, якого треба видалити: ").strip())
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кота з ім'ям '{name}' успішно видалено.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")


def delete_all(cats_collection):
    confirm = clear_input(input("Справді хочете видалити всі записи? (y/n): ").lower().strip())
    if confirm == 'y':
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів(у).")
    else:
        print("Операція скасована.")


def create_record(cats_collection):
    name = clear_input(input("Введіть ім'я кота: ").strip())
    age_str = clear_input(input("Введіть вік кота: ").strip())
    try:
        age = int(age_str)
    except ValueError:
        print("Помилка: вік має бути цілим числом.")
        return
    features_str = clear_input(input("Введіть характеристики (через кому): ").strip())
    if features_str:
        features_list = [f.strip() for f in features_str.split(',')]
    else:
        features_list = []

    new_cat = {
        "name": name,
        "age": age,
        "features": features_list
    }
    result = cats_collection.insert_one(new_cat)
    print(f"Створено нового кота з _id={result.inserted_id}")


def main():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    cats_collection = db[COLLECTION_NAME]

    while True:
        print("\n=== Оберіть дію ===")
        print("1. Показати всі записи")
        print("2. Показати кота за ім'ям")
        print("3. Створити нового кота")
        print("4. Оновити вік кота за ім'ям")
        print("5. Додати характеристику коту за ім'ям")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всі записи")
        print("0. Вихід")

        choice = input("Ваш вибір: ").strip()

        if choice == '1':
            show_all(cats_collection)
        elif choice == '2':
            show_one_by_name(cats_collection)
        elif choice == '3':
            create_record(cats_collection)
        elif choice == '4':
            update_age_by_name(cats_collection)
        elif choice == '5':
            add_feature_by_name(cats_collection)
        elif choice == '6':
            delete_one_by_name(cats_collection)
        elif choice == '7':
            delete_all(cats_collection)
        elif choice == '0':
            print("Вихід із програми.")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")

    client.close()


if __name__ == "__main__":
    main()

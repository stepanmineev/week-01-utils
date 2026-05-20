import csv
import os
import requests


# === Общие функции ===

def ask_required(question):
    answer = input(question).strip()

    if answer == "":
        print("Ошибка: поле нельзя оставлять пустым.")
        exit()

    return answer


def ask_number(question):
    while True:
        answer = ask_required(question)

        try:
            return int(answer)
        except ValueError:
            print("Ошибка: нужно ввести число.")


# === 1. Расчет цены ===

def calculate_price():
    hours = ask_number("Сколько часов займет задача? ")
    rate = ask_number("Сколько рублей стоит 1 час работы? ")
    discount = ask_number("Скидка для первого клиента в процентах? ")

    total = hours * rate
    discount_amount = int(total * discount / 100)
    final_price = int(total - discount_amount)

    print()
    print("Цена без скидки:", total, "руб.")
    print("Скидка:", discount_amount, "руб.")
    print("Итоговая цена:", final_price, "руб.")


# === 2. Бриф клиента ===

def collect_brief():
    name = ask_required("Имя клиента: ")
    business = ask_required("Чем занимается бизнес клиента? ")
    clients = ask_required("Кто его клиенты? ")
    problem = ask_required("Какая повторяющаяся задача отнимает время? ")
    current_process = ask_required("Как клиент решает это сейчас? ")
    deadline = ask_required("Когда нужен результат? ")
    budget = ask_required("Какой бюджет? ")

    print()
    print("=== БРИФ КЛИЕНТА ===")
    print("Клиент:", name)
    print("Бизнес:", business)
    print("Клиенты бизнеса:", clients)
    print("Проблема:", problem)
    print("Как решает сейчас:", current_process)
    print("Срок:", deadline)
    print("Бюджет:", budget)

    with open("brief.txt", "a", encoding="utf-8") as file:
        file.write("=== БРИФ КЛИЕНТА ===\n")
        file.write("Клиент: " + name + "\n")
        file.write("Бизнес: " + business + "\n")
        file.write("Клиенты бизнеса: " + clients + "\n")
        file.write("Проблема: " + problem + "\n")
        file.write("Как решает сейчас: " + current_process + "\n")
        file.write("Срок: " + deadline + "\n")
        file.write("Бюджет: " + budget + "\n")
        file.write("\n---\n\n")

    print()
    print("Бриф сохранен в brief.txt")


# === 3. Сохранение заявки ===

def save_lead():
    file_exists = os.path.exists("leads.csv")

    name = ask_required("Имя клиента: ")
    phone = ask_required("Телефон клиента: ")
    task = ask_required("Задача клиента: ")
    budget = ask_required("Бюджет: ")

    with open("leads.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["name", "phone", "task", "budget"])

        writer.writerow([name, phone, task, budget])

    print()
    print("Заявка сохранена в leads.csv")


# === 4. Просмотр заявок ===

def show_leads():
    if not os.path.exists("leads.csv"):
        print("Файл leads.csv не найден. Сначала добавь хотя бы одну заявку.")
        return

    with open("leads.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print()
        print("=== СПИСОК ЗАЯВОК ===")
        print()

        for row in reader:
            if row["name"] == "" and row["phone"] == "" and row["task"] == "" and row["budget"] == "":
                continue

            print("Клиент:", row["name"])
            print("Телефон:", row["phone"])
            print("Задача:", row["task"])
            print("Бюджет:", row["budget"])
            print("---")


# === 5. Поиск заявки ===

def search_lead():
    if not os.path.exists("leads.csv"):
        print("Файл leads.csv не найден. Сначала добавь хотя бы одну заявку.")
        return

    search_text = ask_required("Введите имя или часть имени клиента: ").lower()
    found = False

    with open("leads.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print()
        print("=== РЕЗУЛЬТАТ ПОИСКА ===")
        print()

        for row in reader:
            if row["name"] == "" and row["phone"] == "" and row["task"] == "" and row["budget"] == "":
                continue

            if search_text in row["name"].lower():
                found = True
                print("Клиент:", row["name"])
                print("Телефон:", row["phone"])
                print("Задача:", row["task"])
                print("Бюджет:", row["budget"])
                print("---")

    if not found:
        print("Заявки с таким клиентом не найдены.")


# === 6. Удаление заявки ===

def delete_lead():
    if not os.path.exists("leads.csv"):
        print("Файл leads.csv не найден. Сначала добавь хотя бы одну заявку.")
        return

    search_text = ask_required("Введите имя или часть имени клиента для удаления: ").lower()
    confirm = ask_required("Точно удалить найденные заявки? Напишите да или нет: ").lower()

    if confirm != "да":
        print("Удаление отменено.")
        return

    remaining_rows = []
    deleted_count = 0

    with open("leads.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["name"] == "" and row["phone"] == "" and row["task"] == "" and row["budget"] == "":
                continue

            if search_text in row["name"].lower():
                deleted_count = deleted_count + 1
            else:
                remaining_rows.append(row)

    with open("leads.csv", "w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "phone", "task", "budget"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(remaining_rows)

    print()
    print("Удалено заявок:", deleted_count)


# === 7. Редактирование заявки ===

def update_lead():
    if not os.path.exists("leads.csv"):
        print("Файл leads.csv не найден. Сначала добавь хотя бы одну заявку.")
        return

    search_text = ask_required("Введите имя или часть имени клиента для изменения: ").lower()
    updated_rows = []
    updated_count = 0

    with open("leads.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["name"] == "" and row["phone"] == "" and row["task"] == "" and row["budget"] == "":
                continue

            if search_text in row["name"].lower():
                print()
                print("Найдена заявка:")
                print("Клиент:", row["name"])
                print("Телефон:", row["phone"])
                print("Задача:", row["task"])
                print("Бюджет:", row["budget"])
                print()
                print("Введите новые данные.")

                row["name"] = ask_required("Новое имя клиента: ")
                row["phone"] = ask_required("Новый телефон клиента: ")
                row["task"] = ask_required("Новая задача клиента: ")
                row["budget"] = ask_required("Новый бюджет: ")

                updated_count = updated_count + 1

            updated_rows.append(row)

    with open("leads.csv", "w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "phone", "task", "budget"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(updated_rows)

    print()
    print("Изменено заявок:", updated_count)


# === 8. Проверка GitHub профиля ===

def check_github_profile():
    username = ask_required("Введите GitHub username: ")
    url = "https://api.github.com/users/" + username
    response = requests.get(url)

    if response.status_code == 404:
        print("Пользователь не найден.")
        return

    if response.status_code != 200:
        print("Ошибка запроса. Код:", response.status_code)
        return

    data = response.json()

    print()
    print("=== GITHUB PROFILE ===")
    print("Логин:", data["login"])
    print("Имя:", data["name"])
    print("Публичные репозитории:", data["public_repos"])
    print("Подписчики:", data["followers"])
    print("Ссылка:", data["html_url"])


# === Главное меню ===

while True:
    print()
    print("=== MINI CRM ДЛЯ ЗАЯВОК ===")
    print("1. Собрать бриф клиента")
    print("2. Посчитать цену услуги")
    print("3. Сохранить заявку в CSV")
    print("4. Показать заявки")
    print("5. Найти заявку по имени")
    print("6. Удалить заявку по имени")
    print("7. Изменить заявку по имени")
    print("8. Проверить GitHub профиль")
    print("0. Выйти из программы")

    choice = input("Выбери действие: ")

    if choice == "1":
        collect_brief()
    elif choice == "2":
        calculate_price()
    elif choice == "3":
        save_lead()
    elif choice == "4":
        show_leads()
    elif choice == "5":
        search_lead()
    elif choice == "6":
        delete_lead()
    elif choice == "7":
        update_lead()
    elif choice == "8":
        check_github_profile()
    elif choice == "0":
        print("Готово. Работа завершена.")
        break
    else:
        print("Ошибка: выбери пункт от 0 до 8.")

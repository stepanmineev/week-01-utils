import csv
import os

file_exists = os.path.exists("leads.csv")

name = input("Имя клиента: ")
if name == "":
    print("Ошибка: имя клиента нельзя оставлять пустым.")
    exit()

phone = input("Телефон клиента: ")
if phone == "":
    print("Ошибка: телефон нельзя оставлять пустым.")
    exit()

task = input("Задача клиента: ")
if task == "":
    print("Ошибка: задачу клиента нельзя оставлять пустой.")
    exit()

budget = input("Бюджет: ")
if budget == "":
    print("Ошибка: бюджет нельзя оставлять пустым.")
    exit()

with open("leads.csv", "a", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["name", "phone", "task", "budget"])

    writer.writerow([name, phone, task, budget])

print()
print("Заявка сохранена в leads.csv")

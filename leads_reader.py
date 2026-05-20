import csv
import os

if not os.path.exists("leads.csv"):
    print("Файл leads.csv не найден. Сначала добавь хотя бы одну заявку.")
    exit()

with open("leads.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)

    print("=== СПИСОК ЗАЯВОК ===")
    print()

    for row in reader:
        print(row)

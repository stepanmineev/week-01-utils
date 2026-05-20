import requests


username = input("Введите GitHub username: ").strip()

if username == "":
    print("Ошибка: username нельзя оставлять пустым.")
    exit()

url = "https://api.github.com/users/" + username
response = requests.get(url)

if response.status_code == 404:
    print("Пользователь не найден.")
    exit()

if response.status_code != 200:
    print("Ошибка запроса. Код:", response.status_code)
    exit()

data = response.json()

print()
print("=== GITHUB PROFILE ===")
print("Логин:", data["login"])
print("Имя:", data["name"])
print("Публичные репозитории:", data["public_repos"])
print("Подписчики:", data["followers"])
print("Ссылка:", data["html_url"])

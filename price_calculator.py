hours = int(input("Сколько часов займет задача? "))
rate = int(input("Сколько рублей стоит 1 час работы? "))
discount = int(input("Скидка для первого клиента в процентах? "))

total = hours * rate
discount_amount = total * discount / 100
final_price = total - discount_amount
discount_amount = int(discount_amount)
final_price = int(final_price)
discount_amount = int(discount_amount)

print()
print("Цена без скидки:", total, "руб.")
print("Скидка:", discount_amount, "руб.")
print("Итоговая цена:", final_price, "руб.")
print("Совет: называй клиенту итоговую цену и объясняй, что входит в работу.")

import asyncio
import json
import random
from datetime import datetime

# Определяем возможные категории для транзакций
categories = ["Food", "Bills", "Entertainment", "Transport", "Shopping"]

# Функция для генерации одной транзакции
def generate_transaction():
    # Получаем текущую дату и время в нужном формате
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Случайным образом выбираем категорию для транзакции
    category = random.choice(categories)
    
    # Генерируем случайную сумму транзакции в пределах от 10 до 500 с точностью до 2 знаков после запятой
    amount = round(random.uniform(10.0, 500.0), 2)
    
    # Возвращаем транзакцию в виде словаря с полями: время, категория и сумма
    return {"timestamp": timestamp, "category": category, "amount": amount}

# Функция для сохранения транзакций в файл формата JSON
async def save_to_file(transactions, file_name="transactions.json"):
    # Открываем файл для записи (перезаписываем его)
    with open(file_name, "a") as f:  # Теперь добавляем данные в конец файла
        # Сохраняем транзакции в формате JSON с отступами для удобства чтения
        json.dump(transactions, f, indent=4)
        f.write("\n")  # Добавляем новую строку для разделения групп
    
    # Выводим в консоль количество сохранённых транзакций и имя файла
    print(f"Сохранено {len(transactions)} транзакций в файл {file_name}")

# Асинхронная функция для генерации списка транзакций
async def generate_transactions(num_transactions):
    transactions = []  # Список для хранения транзакций
    for i in range(num_transactions):
        # Генерируем одну транзакцию и добавляем её в список
        transactions.append(generate_transaction())
        
        # Каждые 10 транзакций сохраняем в файл
        if len(transactions) == 10:
            # Сохраняем текущие транзакции и очищаем список для следующих
            await save_to_file(transactions)
            transactions = []  # Очищаем список транзакций после сохранения
        
    # Если осталось меньше 10 транзакций, сохраняем их тоже
    if transactions:
        await save_to_file(transactions)

# Основной блок программы
if __name__ == "__main__":
    # Запрашиваем у пользователя количество транзакций для генерации
    num_transactions = int(input("Введите количество транзакций для генерации: "))
    
    # Запускаем асинхронную задачу генерации транзакций
    asyncio.run(generate_transactions(num_transactions))

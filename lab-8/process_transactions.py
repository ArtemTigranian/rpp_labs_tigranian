import asyncio
import json
from collections import defaultdict

# Функция для загрузки данных из файла с проверкой на ошибки
async def load_data(file_name="transactions.json"):
    transactions = []  # Список для хранения транзакций
    try:
        with open(file_name, "r") as f:
            # Читаем весь файл и убираем лишние пробелы и пустые строки
            content = f.read().strip()
            
            # Проверяем, чтобы файл не был пустым
            if content:
                # Преобразуем содержимое файла в список Python с использованием JSON
                transactions = json.loads(content)
    except json.JSONDecodeError as e:
        # Если возникла ошибка при декодировании JSON (неправильный формат)
        print(f"Ошибка при чтении JSON из файла: {e}")
    except FileNotFoundError:
        # Если файл не найден
        print(f"Файл '{file_name}' не найден.")
    
    # Возвращаем список транзакций (может быть пустым в случае ошибки)
    return transactions

# Функция для обработки транзакций
async def process_transactions(file_name="transactions.json"):
    # Загружаем данные из файла
    transactions = await load_data(file_name)
    
    # Если транзакций нет, выводим сообщение и завершаем выполнение
    if not transactions:
        print("Нет валидных транзакций для обработки.")
        return

    # Используем defaultdict для хранения суммы по каждой категории
    # default=float означает, что если ключа нет, будет возвращено значение 0.0
    category_sums = defaultdict(float)
    
    # Проходим по всем транзакциям и суммируем значения по категориям
    for transaction in transactions:
        category_sums[transaction["category"]] += transaction["amount"]
    
    # Выводим результаты по каждой категории
    for category, total in category_sums.items():
        print(f"Категория: {category}, Общая сумма: {total}")
        
        # Если расходы по категории превышают 1000, выводим предупреждение
        if total > 1000:
            print(f"Предупреждение: Расходы в категории '{category}' превысили 1000!")

# Главная функция, которая запускает обработку транзакций
if __name__ == "__main__":
    # Запускаем асинхронную задачу для обработки транзакций
    asyncio.run(process_transactions())

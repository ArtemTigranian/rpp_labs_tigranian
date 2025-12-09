import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Создание экземпляра Flask-приложения
app = Flask(__name__)

# Инициализация Flask-Limiter для ограничения частоты запросов
limiter = Limiter(app)

# Устанавливаем максимальный размер запроса (16 МБ)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер запроса

# Функция для загрузки данных из файла data.json при старте приложения
def load_data():
    try:
        # Попытка открыть и загрузить данные из файла
        with open("data.json", "r") as f:
            return json.load(f)  # Возвращаем данные в виде Python-словаря
    except FileNotFoundError:
        # Если файл не найден, возвращаем пустой словарь
        return {}

# Функция для сохранения данных обратно в файл data.json
def save_data(data):
    # Открытие файла для записи
    with open("data.json", "w") as f:
        # Сохраняем данные в формате JSON с отступами для читаемости
        json.dump(data, f, indent=4)

# Загрузка начальных данных в хранилище
data = load_data()

# Маршрут для добавления нового ключа-значения в хранилище
@app.route("/set", methods=["POST"])
@limiter.limit("10 per minute")  # Ограничение на 10 запросов в минуту для /set
def set_key_value():
    # Получаем ключ и значение из JSON-запроса
    key = request.json.get("key")
    value = request.json.get("value")
    
    # Проверяем, что и ключ, и значение присутствуют
    if key is None or value is None:
        return jsonify({"error": "Key and value are required"}), 400  # Ошибка, если чего-то не хватает
    
    # Добавляем или обновляем значение по ключу в хранилище
    data[key] = value
    # Сохраняем измененные данные обратно в файл
    save_data(data)
    # Отправляем успешный ответ
    return jsonify({"message": f"Key '{key}' set with value '{value}'"}), 200

# Маршрут для получения значения по ключу
@app.route("/get/<key>", methods=["GET"])
@limiter.limit("100 per day")  # Ограничение на 100 запросов в сутки для /get
def get_key_value(key):
    # Ищем значение по ключу
    value = data.get(key)
    if value is None:
        return jsonify({"error": "Key not found"}), 404  # Возвращаем ошибку, если ключ не найден
    return jsonify({key: value}), 200  # Возвращаем значение по ключу

# Маршрут для удаления ключа
@app.route("/delete/<key>", methods=["DELETE"])
@limiter.limit("10 per minute")  # Ограничение на 10 запросов в минуту для /delete
def delete_key(key):
    # Проверяем, существует ли ключ в хранилище
    if key in data:
        # Удаляем ключ из хранилища
        del data[key]
        # Сохраняем изменения в файл
        save_data(data)
        return jsonify({"message": f"Key '{key}' deleted"}), 200  # Возвращаем сообщение об успешном удалении
    return jsonify({"error": "Key not found"}), 404  # Возвращаем ошибку, если ключ не найден

# Маршрут для проверки существования ключа в хранилище
@app.route("/exists/<key>", methods=["GET"])
@limiter.limit("100 per day")  # Ограничение на 100 запросов в сутки для /exists
def key_exists(key):
    # Проверяем наличие ключа в хранилище
    if key in data:
        return jsonify({"exists": True}), 200  # Возвращаем True, если ключ существует
    return jsonify({"exists": False}), 200  # Возвращаем False, если ключ отсутствует

# Основной запуск приложения
if __name__ == "__main__":
    # Запуск Flask-приложения с отладчиком на порту 5000
    app.run(debug=True, port=5000)

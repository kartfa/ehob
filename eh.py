import os
import telebot
from datetime import datetime
from flask import Flask

BOT_TOKEN =os.getenv("TGTOK")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# Определяем "пустой" маршрут (route)
@app.route("/")
def hello_world():
    return "Bot is running!"  # Просто возвращаем сообщение

# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def repeat_message(message):
    # Получаем информацию о пользователе
    username = message.from_user.username if message.from_user.username else "Без username"
    first_name = message.from_user.first_name if message.from_user.first_name else "Без имени"
    
    # Получаем текущее время
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Получаем текст сообщения
    message_text = message.text
    
    # Выводим информацию в консоль
    print(f"Новое сообщение, время: {current_time} . От пользователя: {first_name} (@{username}). Текст сообщения: {message_text}")
    
    # Отправляем копию сообщения обратно пользователю
    bot.reply_to(message, message_text)

# Обработчик для других типов контента (фото, стикеры и т.д.)
@bot.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'voice'])
def handle_other_content(message):
    # Получаем информацию о пользователе
    username = message.from_user.username if message.from_user.username else "Без username"
    first_name = message.from_user.first_name if message.from_user.first_name else "Без имени"
    
    # Получаем текущее время
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Определяем тип контента
    content_type = message.content_type
    
    # Выводим информацию в консоль
    print(f"\nНовое сообщение, время: {current_time} . От пользователя: {first_name} (@{username}). Тип контента: {content_type}")
    
    # Отправляем пользователю сообщение о типе контента
    bot.reply_to(message, f"Вы отправили {content_type}. Я могу повторять только текстовые сообщения!")


# Запускаем и бота, и Flask-приложение
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    import threading
    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Запускаем бота (polling) в основном потоке
    bot.infinity_polling()
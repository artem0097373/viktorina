import telebot
from telebot import types

# Токен вашего Telegram-бота
TOKEN = "8838143972:AAHAM57D1cgZtAAkE5hNekmR-5ridGYmM00"
bot = telebot.TeleBot(TOKEN)

# Храним текущий счет пользователей (chat_id: score)
user_scores = {}

QUESTIONS = [
    {
        "photo": "https://ibb.co/G3V1LmHJ",
        "question": "Кто изображён на этой фотографии? ❤️",
        "options": ["рома", "барсук", "2 крутых типа"],
        "correct": "2 крутых типа"
    },
    {
        "photo": "https://ibb.co/wZKPtQtf",
        "question": "Кто это??",
        "options": ["Радик зайчик", "максон", "савелий"],
        "correct": "савелий"
    },
    {
        "photo": "https://ibb.co/ZRxGk6L6",
        "question": "Кто такой есман",
        "options": ["слева", "справа", "я ебу"],
        "correct": "справа"
    },
    {
        "photo": "https://ibb.co/bjyq94LZ",
        "question": "это кто",
        "options": ["рома", "роман", "владелец вафель"],
        "correct": ["рома", "роман", "владелец вафель"]
    },
    {
        "photo": "https://ibb.co/YTJxmDtJ",
        "question": "Кто его фоткал?",
        "options": ["радик", "лысый", "илюха чаевский"],
        "correct": "илюха чаевский"
    },
    {
        # Вопрос без фотографии
        "question": "хочешь чтобы я продолжил?",
        "options": ["да", "конечно"],
        "correct": ["да", "конечно"]
    },
    {
        "photo": "https://ibb.co/5XmQrM9W",
        "question": "Кто изображен тут?",
        "options": ["тоустый", "радик", "опущенный"],
        "correct": ["радик"]
    },
    {
        "photo": "https://ibb.co/G4x81XV0",
        "question": "Кто это?",
        "options": ["босс", "барсук", "папочка"],
        "correct": ["босс", "барсук", "папочка"]
    },
    {
        "photo": "https://ibb.co/ync7pZGm",
        "question": "с кем тут рома",
        "options": ["с сучкой", "с малышечкой", "я ебу"],
        "correct": ["с сучкой", "с малышечкой"]
    },
    {
        "photo": "https://ibb.co/BHXw5fhZ",
        "question": "что барсук увидел в телефоне?",
        "options": ["фотку ромы", "радика", "есмана"],
        "correct": ["фотку ромы"]
    },
    {
        "photo": "https://ibb.co/xwhF128",
        "question": "это друг ромы?",
        "options": ["да", "нет"],
        "correct": ["да"]
    },
    {
        "photo": "https://ibb.co/Dfz2T5mB",
        "question": "Последний вопрос: вы знаете его?",
        "options": ["да это рома", "не рома 100%"],
        "correct": ["да это рома"]
    },
    {
        # Вопрос без фотографии
        "question": "Тебе понравилось?",
        "options": ["да"],
        "correct": ["да"]
    }
]

@bot.message_handler(commands=['start'])
def start_quiz(message):
    """Обработчик команды /start для начала викторины."""
    chat_id = message.chat.id
    user_scores[chat_id] = 0  # Сбрасываем счетчик очков
    send_question(chat_id, question_index=0)

def send_question(chat_id, question_index):
    """Отправка текущего вопроса и кнопок с вариантами ответов."""
    if question_index < len(QUESTIONS):
        q = QUESTIONS[question_index]
        
        # Создаем интерактивные кнопки
        markup = types.InlineKeyboardMarkup()
        for idx, option in enumerate(q["options"]):
            # Передаем индекс вопроса и индекс варианта ответа
            callback_data = f"ans_{question_index}_{idx}"
            markup.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))
            
        caption = f"<b>Вопрос {question_index + 1}/{len(QUESTIONS)}</b>\n\n{q['question']}"
        
        # Если у вопроса есть фото, отправляем его
        if "photo" in q and q["photo"]:
            try:
                bot.send_photo(chat_id, q["photo"], caption=caption, reply_markup=markup, parse_mode="HTML")
            except Exception:
                # В случае недоступности фото высылаем только текст
                bot.send_message(chat_id, caption, reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(chat_id, caption, reply_markup=markup, parse_mode="HTML")
    else:
        # Завершение теста
        score = user_scores.get(chat_id, 0)
        total = len(QUESTIONS)
        bot.send_message(
            chat_id, 
            f"🎉 <b>Тест пройден!</b>\n\nПравильных ответов: <b>{score} из {total}</b>! ❤️\n\nТы отлично знаешь Рому!",
            parse_mode="HTML"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    """Обработчик нажатия на кнопки с ответами."""
    chat_id = call.message.chat.id
    data = call.data.split('_')
    q_index = int(data[1])
    opt_index = int(data[2])
    
    q = QUESTIONS[q_index]
    user_answer = q["options"][opt_index]
    correct = q["correct"]
    
    # Приводим верный ответ к единому типу (списку)
    if isinstance(correct, str):
        correct_answers = [correct]
    else:
        correct_answers = correct
    
    # Проверяем ответ
    if user_answer in correct_answers:
        user_scores[chat_id] = user_scores.get(chat_id, 0) + 1
        bot.answer_callback_query(call.id, "Верно! 💕")
    else:
        display_correct = ", ".join(correct_answers)
        bot.answer_callback_query(call.id, f"Упс! Правильный ответ: {display_correct} 💔", show_alert=True)
        
    # Удаляем клавиатуру кнопок у отвеченного вопроса
    try:
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except Exception:
        pass
    
    # Отправляем следующий вопрос
    send_question(chat_id, question_index=q_index + 1)

if __name__ == "__main__":
    print("Бот-тест успешно запущен!")
    bot.infinity_polling(skip_pending=True)
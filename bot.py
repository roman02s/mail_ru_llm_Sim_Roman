import logging
import os

import telebot
from dotenv import load_dotenv
from telebot import types

from src.model_wrapper import ModelWrapper

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler('./logs/bot.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TGTOKEN")
bot = telebot.TeleBot(TOKEN)

model_wrapper = ModelWrapper()  # Внутри класса описание


@bot.message_handler(commands=["help"])
def help(message):
    help_message = """
    Доступны следующие команды:
    /start - старт бота
    /model - выбор модели
    /checkmodel - посмотреть, как модель сейчас загружена
    /generate - сгенерировать текст по контексту (можно использовать без введения команды)
    """
    bot.send_message(message.from_user.id, help_message)
    logger.info("Help command processed.")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.from_user.id,
        "Привет! Для знакомства с доступными командами введите /help",
    )
    logger.info("Start command processed.")


@bot.message_handler(commands=["model"])
def model(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("StatLM")
    btn2 = types.KeyboardButton("GPT")
    btn3 = types.KeyboardButton("Llama")
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.from_user.id, "Выберите модель для генерации", reply_markup=markup
    )
    logger.info("Model selection displayed.")


@bot.message_handler(commands=["checkmodel"])
def checkmodel(message):
    current_model = str(model_wrapper.current_model_name)
    bot.send_message(message.from_user.id, f"Текущая модель: {current_model}")
    logger.info(f"Checked current model: {current_model}")


@bot.message_handler(commands=["generate"])
def generate(message):
    bot.send_message(
        message.from_user.id,
        "Введите текст (вопрос, на который нужно ответить, либо текст, который нужно продолжить)",
    )
    logger.info("Generate command initiated.")


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    logger.debug(f"Received message: {message.text}")
    if message.text in ["StatLM", "GPT", "Llama"]:
        logger.debug(f"Model selection: {message.text}")
        status, result = model_wrapper.load(message.text, test_inference=True)
        if status:
            bot.send_message(message.from_user.id, "Подгружено")
            logger.info(f"Model {message.text} loaded successfully.")
        else:
            bot.send_message(
                message.from_user.id,
                f"Проблемы с загрузкой модели, ниже описаны ошибки.\n{result}",
            )
            logger.error(f"Error loading model {message.text}: {result}")
    else:
        status, result = model_wrapper.generate(message.text)
        if status:
            bot.send_message(message.from_user.id, result)
            logger.info("Text generated successfully.")
        else:
            bot.send_message(
                message.from_user.id,
                f"Проблемы с генерацией, ниже описаны ошибки.\n{result}",
            )
            logger.error(f"Error generating text: {result}")


bot.polling(none_stop=True, interval=0)

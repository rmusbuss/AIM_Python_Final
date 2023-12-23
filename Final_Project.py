import telebot
import sys
import config
import requests


def get_crypto_price_by_name(crypto_name):
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"/simple/price?ids={crypto_name}&vs_currencies=usd"
    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if crypto_name in data and "usd" in data[crypto_name]:
            crypto_price = data[crypto_name]["usd"]
            return crypto_price
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def starting_message(message):
    bot.send_message(
        message.chat.id,
        "Hello, {0.first_name}!\nI am - {1.first_name}\n"
        "I am stock notifier bot\n"
        "Following commands available:\n"
        "Enter /check_price and then type the cryptocurrency name for which you want to know the price\n"
        "To stop bot enter:\n"
        "/stop  /end\n\n".format(message.from_user, bot.get_me()),
    )


if __name__ == "__main__":
    bot = telebot.TeleBot(config.TOKEN)

    @bot.message_handler(commands=["start", "begin"])
    def welcome(message):
        starting_message(message)

    @bot.message_handler(commands=["check_price"])
    def check_price_handler(message):
        global tickers
        chat_id = message.chat.id
        message_price = "enter the cryptocurrency name. For example, **bitcoin**"
        bot.send_message(chat_id, message_price)
        bot.register_next_step_handler(message, check_price)

    def check_price(message):
        global tickers
        chat_id = message.chat.id

        crypto_name = message.text.lower()
        crypto_price = get_crypto_price_by_name(crypto_name)
        message_price = crypto_name + " price is " + str(crypto_price) + " usd"
        bot.send_message(chat_id, message_price)

    @bot.message_handler(commands=["stop", "end"])
    def handle_stop(message):
        bot.send_message(message.chat.id, "Bot is stopped")
        sys.exit()

    bot.polling(none_stop=True)

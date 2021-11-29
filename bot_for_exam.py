import telebot
import requests
import time
from bs4 import BeautifulSoup

token = "2144114202:AAFXkl0n-EyhmWd41UvzwNL_GzAifuQy3Dg"
channel_id = "@linkfordisnuz"
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == "Старт":
        bot.send_message(channel_id, "Новая новость!!!!")
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(channel_id, post_text[0])
                time.sleep(180)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")


def parser(back_post_id):
    URL = "https://kaktus.media"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("div", class_="Dashboard-Board--content")
    post_id = post.find('span', class_='Dashboard-Content-Card--countComments tolstoy-comments-count')['data-identity']

    if post_id != back_post_id:
        title = post.find("a", class_="Dashboard-Content-Card--name").text.strip()

        url = post.find("a", class_="Dashboard-Content-Card--name", href=True)['href'].strip()

        return f"{title}\n\n{url}", post_id
    else:
        return None, post_id


bot.polling()

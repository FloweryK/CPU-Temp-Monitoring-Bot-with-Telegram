import telegram
from telegram.ext import Updater, CommandHandler


class TelegramBot:
    def __init__(self, name, token, id):
        self.name = name
        self.core = telegram.Bot(token)
        self.id = id
        self.updater = Updater(token, use_context=True)

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)

    def sendPhoto(self, photo_path):
        self.core.sendPhoto(chat_id=self.id, photo=open(photo_path, 'rb'))

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()


class Fairy(TelegramBot):
    def __init__(self, token, id):
        TelegramBot.__init__(self, name='서버 요정', token=token, id=id)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def add_schedule(self, func, interval):
        self.updater.job_queue.run_repeating(func, interval=interval, first=0)

    def start(self):
        self.sendMessage('서버 요정이 잠에서 깨어납니다.')
        self.updater.start_polling()
        self.updater.idle()


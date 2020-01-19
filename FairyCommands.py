# encoding: utf-8
from funcs import *
import ChatBotModel

import argparse
import matplotlib.pyplot as plt
from telegram.ext import CallbackContext

import pandas as pd
pd.set_option('display.float_format', lambda x: '%i' % x)


def get_temperatures(delay=1):
    today = load(path_list('history/')[-1])
    now_temp = today.iloc[-delay]
    max_temp = today.iloc[:-delay].max()
    min_temp = today.iloc[:-delay].min()
    avg_temp = today.iloc[:-delay].mean()

    df = pd.DataFrame({
        'now': now_temp,
        'max': max_temp,
        'min': min_temp,
        'avg': avg_temp
    })

    df = df.iloc[:-2]

    return df


def echo(bot, update):
    fairy.sendMessage('에코오오!')


def report_temperatures(bot, update):
    fairy.sendMessage('report temperature 명령 받음!')
    df = get_temperatures()
    fairy.sendMessage(df.to_string())


def draw_temperatures(bot, update):
    fairy.sendMessage('draw temperature 명령 받음!')

    history = []
    for path in path_list('history/')[-7:]:
        history.append(load(path))
    history = pd.concat(history)

    timestamp = history['timestamp'] + 9 * 60 * 60
    date = pd.to_datetime(timestamp, unit='s')

    temp = history.iloc[:, 4:-1]

    plt.plot(date, temp.min(axis=1), label='min temp')
    plt.plot(date, temp.max(axis=1), label='max temp')
    plt.plot(date, temp.mean(axis=1), label='avg temp')

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(rotation=45)
    plt.xlabel('month-day hour')
    plt.ylabel('temperature (C)')

    plt.savefig('draw_temperature.png', bbox_inches='tight')
    plt.close()

    fairy.sendPhoto(photo_path='draw_temperature.png')


def callback_30min(context: CallbackContext):
    fairy.sendMessage('30 min 보고!')
    df = get_temperatures()
    fairy.sendMessage(df.to_string())


def callback_max_alarm(context: CallbackContext):
    today = load(path_list('history/')[-1])
    today = today.drop(['time', 'timestamp'], axis=1)

    max_temp_now = today.max()
    max_temp_5min = today.iloc[:-3*5].max()

    is_max = max_temp_now > max_temp_5min
    print(is_max)

    if True in is_max.values:
        fairy.sendMessage('***** 경고! *****')

        tmp_df = pd.DataFrame({
            'is_max': is_max,
            'max_now': max_temp_now,
            'max_before': max_temp_5min
        })

        fairy.sendMessage(tmp_df.to_string())


if __name__ == '__main__':
    # argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, default='MC', help='user id')
    parser.add_argument('-t', type=str, default='MC', help='token')
    args = parser.parse_args()

    id = args.i
    token = args.t

    # define fairy
    fairy = ChatBotModel.Fairy(token=token, id=id)

    # add schedule
    fairy.add_schedule(callback_30min, interval=60*30)
    fairy.add_schedule(callback_max_alarm, interval=60*5)

    # add commands
    fairy.add_handler('echo', echo)
    fairy.add_handler('report', report_temperatures)
    fairy.add_handler('draw', draw_temperatures)

    # start fairy
    fairy.start()

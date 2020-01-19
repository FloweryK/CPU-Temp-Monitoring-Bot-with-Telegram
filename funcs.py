import pickle
import json
import os
import numpy as np
import datetime
import time


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def save(data, path, name=False):
    start = time.time()

    if name:
        print('saving', name, '.....', end='')

    if path[-4:] == 'json':
        with open(path, 'w', encoding='UTF8') as f:
            json.dump(data, f, ensure_ascii=False)
    else:
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    if name:
        print('complete (%.2fs).' % (time.time() - start))


def load(path, name=False):
    start = time.time()

    if name:
        print('loading', name, '.....', end='')

    if path[-4:] == 'json':
        with open(path, encoding='UTF8') as f:
            result = json.load(f)
    else:
        with open(path, 'rb') as f:
            result = pickle.load(f)

    if name:
        print('complete (%.2fs).' % (time.time() - start))

    return result


def file_list(path):
    try:
        return sorted(os.listdir(path))
    except FileNotFoundError:
        print(path + 'not found')
        return False


def path_list(dir, filter=False, reverse=False):
    try:
        if filter:
            return [dir + '/' + p for p in sorted(os.listdir(dir), reverse=reverse) if filter in p]
        else:
            return [dir + '/' + p for p in sorted(os.listdir(dir), reverse=reverse)]
    except FileNotFoundError:
        print(dir + 'not found')
        return False


def strftime(form='%Y%m%d-%H:%M:%S'):
    return datetime.datetime.now().strftime(form)


class Timer:
    def __init__(self):
        self.history = {
            'start': time.time()
        }

    def initialize(self):
        self.history['start'] = time.time()

    def add_history(self, name):
        self.history[name] = time.time() - self.start

    def report(self):
        for name, time_after_init in self.history.items():
            print(name, ':', time_after_init)


class Eta:
    def __init__(self, total):
        self.start_time = 0
        self.total = total
        self.ticks = []

    def initialize(self):
        self.start_time = time.time()
        self.ticks.append(0.0)

    def progress(self):
        self.ticks.append(time.time() - self.start_time)

    def show(self):
        x = np.arange(0, len(self.ticks))
        y = self.ticks
        coeff = np.polyfit(x, y, 1)

        remaining_secs = (coeff[0] * self.total + coeff[1]) - self.ticks[-1]
        remaining_time = datetime.timedelta(seconds=remaining_secs)
        progress_percent = 100 * (len(self.ticks) - 1) / self.total

        print('ETA:', remaining_time, '(%i%%)' % progress_percent)


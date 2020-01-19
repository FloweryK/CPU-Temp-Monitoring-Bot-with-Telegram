from funcs import *
import re
import subprocess
import pandas as pd
import datetime
import time


def get_temperatures():
    disks = ["/dev/sda1", "/dev/sda2", "/dev/sda3", "/dev/sda4", "/dev/sdb1", ]

    sensors = subprocess.check_output("sensors")

    temperatures = {'time': datetime.datetime.now(),
                    'timestamp': time.time()}

    matches = re.findall("^(.*?)\:\s+\+?(.*?)°C", sensors.decode('utf-8'), re.MULTILINE)
    for match in matches:
        temperatures[match[0]] = float(match[1])

    print(pd.Series(temperatures))

    return temperatures


def write_temperatures(temperatures):
    date = datetime.datetime.now().strftime('%Y%m%d')

    try:
        df = load('history/' + date + '.df')
        df.loc[df.index.max() + 1] = temperatures
    except FileNotFoundError:
        df = pd.DataFrame(temperatures, index=[0])

    save(df, 'history/' + date + '.df')


if __name__ == '__main__':
    mkdir('history/')

    while True:
        temperatures = get_temperatures()
        write_temperatures(temperatures)
        time.sleep(60)

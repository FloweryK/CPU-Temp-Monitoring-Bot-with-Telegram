# Server Fairy: Cpu Temperature Monitoring Telegram Bot

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

#### Prerequisites

```python
certifi==2019.9.11
cffi==1.13.2
cryptography==2.8
cycler==0.10.0
future==0.18.2
kiwisolver==1.1.0
matplotlib==3.1.2
numpy==1.17.4
pandas==0.25.3
pycparser==2.19
pyparsing==2.4.5
python-dateutil==2.8.1
python-telegram-bot==12.2.0
pytz==2019.3
six==1.13.0
tornado==6.0.3

```



#### (Optional) Virtual environment setting

```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```



## Running the tests

You should first prepare 2 screens: One for writing CPU temperature histories, and the other for Telegram Bot - Server Fairy.

```bash
# screen 1
(venv) $ python3 cpuTempWriter.py
# screen 2
(venv) $ python3 FairyCommands.py
user id: <user id>
bot token: <bot token>
```



## References 

텔레그램 봇을 등록하여 만들고싶다면: [python으로 telegram bot 활용하기 - 1 기본 설정편](https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html)

텔레그램 봇의 작동 방식을 알고싶다면: [[챗봇 만들기] 30분 만에 텔레그램 봇 만들기](https://steemit.com/kr-dev/@maanya/30)

리눅스 Screen을 사용해보고싶다면: [How to Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)


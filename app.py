from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os
import json

# config
today = datetime.today()
template_id = os.environ['TEMP_ID']
wechat_app_id = os.environ['APPID']
wechat_app_secret = os.environ['APPSECRET']
user_id = os.environ['WECHAT_ID']
anniversaries = os.environ['ANNIVERSARIES']
custom_date = os.environ['CUSTOM_DATE']
custom_date_time = os.environ['CUSTOM_DATE_TIME']
birthday = os.environ['BIRTHDAY']
repidKey = os.environ['REPID_API_KEY']
repidHost = os.environ['REPID_API_SECRETE']


# content
def get_weather_msg() -> str:
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": "Auckland"}

    headers = {
        "X-RapidAPI-Key": repidKey,
        "X-RapidAPI-Host": repidHost
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    msg = '现在奥克兰%s摄氏度, %s。' % (response['current']['temp_c'], response['current']['condition']['text'])
    return msg


def get_birthday_countdown() -> int:
    next_birthday = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next_birthday < datetime.now():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days


def get_custom_date_countdown() -> int:
    custom_datetime = datetime.strptime(custom_date_time, "%Y-%m-%d")
    return (custom_datetime - today).days


def get_anniversaries() -> int:
    delta = today - datetime.strptime(anniversaries, "%Y-%m-%d")
    return delta.days


def main():
    client = WeChatClient(wechat_app_id, wechat_app_secret)
    wm = WeChatMessage(client)
    payload = {
        "weatherMessages": {"value": get_weather_msg()},
        "countdownDays": {"value": get_anniversaries()},
        "CustomDate": {"value": custom_date},
        "countdownCustomDate": {"value": get_custom_date_countdown()},
        "countdownBirthDay": {"value": get_birthday_countdown()}
    }
    res = wm.send_template(user_id, template_id, payload)
    print(res)


main()

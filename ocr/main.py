from BaiduOCR import BaiduOCR
from cut import Screenshot
import pyperclip
import os
from pystray import MenuItem
from PIL import Image
import pystray
import threading
import keyboard
import sys
import requests
import subprocess

event = threading.Event()
user_path = os.path.expanduser("~")
sgpt_path = os.path.join(user_path, "sgpt")


def click_menu(icon, item):
    if item == menu[0]:
        if getattr(sys, "frozen", False):
            # 如果是可执行文件，则获取可执行文件所在的目录
            base_dir = sys._MEIPASS
        else:
            # 如果是脚本文件，则获取脚本文件所在的目录
            base_dir = os.path.abspath(os.path.dirname(__file__))
        image = Image.open(f"{base_dir}\\OneClickQuery.ico")
        icon.icon = image
        main()


def on_exit(icon, item):
    icon.stop()


def main():
    Screenshot.main()
    temp_var = os.environ.get("TEMP")
    try:
        img = BaiduOCR.get_file_content_as_base64(f"{temp_var}\\Screenshot.png")
    except FileNotFoundError:
        return
    os.remove(f"{temp_var}\\Screenshot.png")
    result = BaiduOCR.main(img)
    print("AI正在思考中...")
    if getattr(sys, "frozen", False):
        # 如果是可执行文件，则获取可执行文件所在的目录
        base_dir = sys._MEIPASS
    else:
        # 如果是脚本文件，则获取脚本文件所在的目录
        base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        user_msg = f"这里有一道题，请只告诉我答案，不需要解释，这是题目:{result}"
        result = chat(user_msg)
    except:
        result = "程序错误，请重试"
    if result:
        pyperclip.copy(result)
    else:
        pyperclip.copy("程序错误，请重试")
    image = Image.open(f"{base_dir}\\active.ico")
    icon.icon = image


def shot(event):
    while not event.is_set():
        if keyboard.is_pressed("ctrl+q"):
            if getattr(sys, "frozen", False):
                # 如果是可执行文件，则获取可执行文件所在的目录
                base_dir = sys._MEIPASS
            else:
                # 如果是脚本文件，则获取脚本文件所在的目录
                base_dir = os.path.abspath(os.path.dirname(__file__))
            image = Image.open(f"{base_dir}\\OneClickQuery.ico")
            icon.icon = image
            main()


def tary(event):
    icon.run()
    event.set()


def chat(user_msg):
    api_key = ""

    url = "https://openai.api2d.net/v1/chat/completions"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_msg}],
    }

    response = requests.post(url, headers=headers, json=data)

    response_json = response.json()
    content = response_json["choices"][0]["message"]["content"]
    return content


menu = (
    MenuItem(text="OCR(curl+Q)", action=click_menu, default=True, visible=True),
    MenuItem(text="退出", action=on_exit),
)
if getattr(sys, "frozen", False):
    # 如果是可执行文件，则获取可执行文件所在的目录
    base_dir = sys._MEIPASS
else:
    # 如果是脚本文件，则获取脚本文件所在的目录
    base_dir = os.path.abspath(os.path.dirname(__file__))
image = Image.open(f"{base_dir}\\OneClickQuery.ico")
icon = pystray.Icon("name", image, "ocr2sgpt", menu)
subprocess.Popen([f"{sgpt_path}/Ditto/Ditto.exe"])

t1 = threading.Thread(target=shot, args=(event,))
t2 = threading.Thread(target=tary, args=(event,))
t1.start()
t2.start()
t1.join()
t2.join()

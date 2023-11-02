from BaiduOCR import BaiduOCR
from cut import Screenshot
import pyperclip
import os
import json
from pystray import MenuItem
from PIL import Image
import pystray
import threading
import keyboard
import sys
import requests
import subprocess
import shutil
from bs4 import BeautifulSoup
import psutil

event = threading.Event()
user_path = os.path.expanduser("~")
OneClickQuery_path = os.path.join(user_path, "OneClickQuery")
searchEngine = "题库"


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
    elif item == menu[1]:
        global searchEngine
        if searchEngine == "题库":
            searchEngine = "AI"
        else:
            searchEngine = "题库"
        print(f"已切换到{searchEngine}")
        pyperclip.copy(f"已切换到{searchEngine}")


def on_exit(icon):
    try:
        ditto_processes = []
        for process in psutil.process_iter():
            try:
                proc_info = process.as_dict(attrs=["pid", "name"])
                if proc_info["name"].lower() == "ditto.exe":
                    ditto_processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        processes = ditto_processes
        for proc in processes:
            psutil.Process(proc["pid"]).terminate()
    except:
        pass
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
    print(result)
    if getattr(sys, "frozen", False):
        # 如果是可执行文件，则获取可执行文件所在的目录
        base_dir = sys._MEIPASS
    else:
        # 如果是脚本文件，则获取脚本文件所在的目录
        base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        if searchEngine == "题库":
            result = tiku(result)
        else:
            user_msg = f"这里有一道题，请解答并只告诉我答案，不需要解释，这是题目:{result}"
            result = chat(user_msg)
    except:
        result = "程序错误，请重试"
    if result:
        print(result)
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


def tiku(result):
    tk_token = ""
    version = "2.0.3"
    question = result

    url = "https://app.itihey.com/pcService/api/queryAnswer"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "access-token": tk_token,
        "Version": version,
    }
    data = {
        "word": question,
        "location": "https://baidu.com",
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).text
    soup = BeautifulSoup(response, "html.parser")
    page = soup.findAll("div", class_="page")[1]
    # 获取所有的div标签
    list_div = page.findAll("div", class_="list-item")
    # 遍历div标签
    i = 1
    display_text = ""
    for div in list_div:
        title = f"题目{i}：" + div.findAll("span", class_="text_4")[0].text
        answer = div.find("div", class_="text_8").text.replace(" ", "")
        option = (
            div.findAll("span", class_="text_4")[1]
            .text.replace(" ", "")
            .replace("　", "")
        )
        lines = option.strip().split("\n")
        for line in lines:
            if line.startswith("D"):
                answer = "答案：" + line.replace(" ", "").replace("　", "")
        display_text += (
            title + "\n" + answer + "\n" + option + "\n" + "------------------" + "\n"
        )
        i += 1
    return display_text


menu = (
    MenuItem(text="OCR(curl+Q)", action=click_menu, default=True, visible=True),
    MenuItem(text="切换搜索源", action=click_menu, default=False, visible=True),
    MenuItem(text="退出", action=on_exit),
)
if getattr(sys, "frozen", False):
    # 如果是可执行文件，则获取可执行文件所在的目录
    base_dir = sys._MEIPASS
else:
    # 如果是脚本文件，则获取脚本文件所在的目录
    base_dir = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(OneClickQuery_path):
    os.makedirs(OneClickQuery_path)
    shutil.copytree(f"{base_dir}\\Ditto", f"{OneClickQuery_path}/Ditto")
image = Image.open(f"{base_dir}\\OneClickQuery.ico")
icon = pystray.Icon("name", image, "OneClickQuery", menu)
subprocess.Popen([f"{OneClickQuery_path}/Ditto/Ditto.exe"])
print(f"当前搜索源为{searchEngine}")

t1 = threading.Thread(target=shot, args=(event,))
t2 = threading.Thread(target=tary, args=(event,))
t1.start()
t2.start()
t1.join()
t2.join()

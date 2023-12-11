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
import psutil
from collections import Counter

event = threading.Event()
user_path = os.path.expanduser("~")
searchEngine = "题库"
if getattr(sys, "frozen", False):
    # 如果是可执行文件，则获取可执行文件所在的目录
    base_dir = sys._MEIPASS
else:
    # 如果是脚本文件，则获取脚本文件所在的目录
    base_dir = os.path.abspath(os.path.dirname(__file__))


def click_menu(icon, item):
    if item == menu[0]:
        main(icon)
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


def main(icon):
    image = Image.open(f"{base_dir}\\OneClickQuery.ico")
    icon.icon = image
    Screenshot.main()
    temp_var = os.environ.get("TEMP")
    try:
        img = BaiduOCR.get_file_content_as_base64(f"{temp_var}\\Screenshot.png")
    except FileNotFoundError:
        return
    os.remove(f"{temp_var}\\Screenshot.png")
    try:
        result = BaiduOCR.main(img)
    except:
        return
    print(result)
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
            main(icon)


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


def most_common_answer(answers):
    flat_answers = sum(answers, [])
    # 计算每个答案出现的次数
    answer_counts = Counter(flat_answers)
    # 找出出现次数最多的答案
    most_common = answer_counts.most_common(1)
    if most_common:
        # 返回出现次数最多的答案
        return most_common[0][0]
    else:
        # 如果没有答案，返回 None
        return None


def tiku(result):
    question = result
    tk_token = ""
    url = f"http://lyck6.cn/scriptService/api/autoAnswer/{tk_token}"
    data = {"question": question}
    try:
        response = requests.post(url, json=data).json()["result"]["answers"]
        answers = ""
        for i in response:
            answers += f"{i[0]}\n"
        display_text = f"{question}\n答案：{most_common_answer(response)}\n--------------------\n其他答案：{answers}"
    except:
        display_text = "程序错误，请重试"
    return display_text


menu = (
    MenuItem(text="举手", action=click_menu, default=False, visible=True),
    MenuItem(text="联系老师", action=click_menu, default=False, visible=True),
    MenuItem(text="关于", action=on_exit),
)

image = Image.open(f"{base_dir}\\OneClickQuery.ico")
icon = pystray.Icon("JYdianzijiaoshi", image, "极域学生管理系统", menu)
subprocess.Popen([f"{base_dir}\\Ditto\\Ditto.exe"])
print(f"当前搜索源为{searchEngine}")

t1 = threading.Thread(target=shot, args=(event,))
t2 = threading.Thread(target=tary, args=(event,))
t1.start()
t2.start()
t1.join()
t2.join()

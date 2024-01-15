from BaiduOCR import BaiduOCR
from cut import Screenshot
import os
from pystray import MenuItem
from PIL import Image
import pystray
import threading
import keyboard
import sys
import requests
from collections import Counter
from show import TooltipListWidget
import pyperclip

final_data = []
event = threading.Event()
user_path = os.path.expanduser("~")
searchEngine = "题库"
if getattr(sys, "frozen", False):
    # 如果是可执行文件，则获取可执行文件所在的目录
    base_dir = sys._MEIPASS
else:
    # 如果是脚本文件，则获取脚本文件所在的目录
    base_dir = os.path.abspath(os.path.dirname(__file__))


def change_searchEngine():
    global searchEngine
    if searchEngine == "题库":
        searchEngine = "AI"
    else:
        searchEngine = "题库"
    print(f"已切换到{searchEngine}")
    final_data.insert(0, f"已切换到{searchEngine}")


def on_exit(icon):
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
        print("程序错误，请重试")
        final_data.insert(0, "程序错误，请重试")
        return
    try:
        if searchEngine == "题库":
            result, most_answer = tiku(result)
        else:
            user_msg = f"这里有一道题，请解答并只告诉我答案，不需要解释，这是题目:{result}"
            result = chat(user_msg)
    except:
        result = "程序错误，请重试"
    if result:
        print(result)
        final_data.insert(0, result)
        if searchEngine == "题库":
            pyperclip.copy(most_answer)
        elif searchEngine == "AI":
            pyperclip.copy(result)
    else:
        final_data.insert(0, "程序错误，请重试")
    image = Image.open(f"{base_dir}\\active.ico")
    icon.icon = image


def shot(event):
    def on_hotkey():
        if not event.is_set():
            main(icon)

    keyboard.add_hotkey("ctrl+q", on_hotkey)
    # 阻塞，直到 "ctrl+q" 组合键被按下
    keyboard.wait("ctrl+q")


def tary(event):
    icon.run()
    event.set()


def show_listener(event):
    def on_hotkey():
        if keyboard.is_pressed("ctrl+`"):
            global final_data
            # 始终限制final_data最多5个元素
            final_data = final_data[:5]
            TooltipListWidget.main(final_data)

    keyboard.add_hotkey("ctrl+`", on_hotkey)
    # 阻塞，直到 "ctrl+`" 组合键被按下
    keyboard.wait("ctrl+`")


def chat(user_msg):
    api_key = ""
    url = "https://chat-api.pkcsublog.top/v1/chat/completions"
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
        most_answer = most_common_answer(response)
        display_text = (
            f"{question}\n答案：{most_answer}\n--------------------\n其他答案：{answers}"
        )
    except:
        display_text = "程序错误，请重试"
    return display_text, most_answer


menu = (
    MenuItem(text="举手", action=main, default=False, visible=True),
    MenuItem(text="联系老师", action=change_searchEngine, default=False, visible=True),
    MenuItem(text="关于", action=on_exit),
)

image = Image.open(f"{base_dir}\\OneClickQuery.ico")
icon = pystray.Icon("JYdianzijiaoshi", image, "极域学生管理系统", menu)
print(f"当前搜索源为{searchEngine}")

t1 = threading.Thread(target=shot, args=(event,))
t2 = threading.Thread(target=tary, args=(event,))
t3 = threading.Thread(target=show_listener, args=(event,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

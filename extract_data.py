import re
import time
import json
import spacy
import random
import selenium
import pyautogui
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from youtubesearchpython import VideosSearch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

overall_clf = spacy.load("Overall_model")
game_clf = spacy.load("Game_model")
sa_clf = spacy.load("Chat_model")

overall_topic = ["轉播", "加油", "閒聊"]

def model(text):
    result = {}
    o = overall_clf(text).cats
    for topic in overall_topic:
        result[topic] = o[topic]
    g = game_clf(text).cats
    sa = sa_clf(text).cats
    result.update(g)
    result.update(sa)
    
    return result

def extract_data(input_data):

    entries = input_data.split('\r\n\r\n')

    for entry in entries:

        if not entry:
            continue

        if entry not in history:

            history.append(entry)

            match = re.match(r'((?:\d{1,2}:)?\d{1,2}:\d{1,2})\r\n(.+)\r\n\u200b\u200b(.+)', entry)
            
            if match:
                timestamp = match.group(1)
                username = match.group(2)
                content = re.sub(r"\u200d", "", match.group(3))

                entry_dict = {
                    "time": timestamp,
                    "user": username,
                    "content": content
                }

                result = model(content)
                entry_dict.update(result)

                extracted_data.append(entry_dict)

                print(entry_dict, end = "\r")

    return extracted_data

def ctrl_a():
    pyautogui.hotkey('ctrl', 'a')


def ctrl_c():
    pyautogui.hotkey('ctrl', 'c')

def speed_up():
    pyautogui.press('right')

def read_clipboard():
    clipboard_content = pyperclip.paste()
    clipboard_content = re.sub(r"\r\n\r\n已啟用聊天室訊息重播功能。直播時的所有聊天室訊息都會顯示在這裡。", '', clipboard_content)
    return clipboard_content

no_comment = [2, 3, 16, 43, 44, 45, 53, 62, 77]
missing = [42, 50, 51,59, 64, 87, 73, 75,97, 108, 112, 115]
target = list(i for i in range(1, 40) if i not in no_comment)

for game in target:
    videosSearch = VideosSearch(f'G{game}【FIRE】企業19年甲級男女排球聯賽', limit = 1)

    driver = webdriver.Chrome()
    url = videosSearch.result()['result'][0]['link']
    driver.get(url)

    time.sleep(10)

    any_YT_position = [1259, 286]
    play_position = [543, 606]
    setting_position = [755, 833]
    speed = [766, 672]
    def_speed = [942, 461]
    x2_position = [924, 669]
    qua_position = [773, 739]
    qua_scroll_down = [986, 770]
    low_144p = [683, 679]
    chat_setting = [1408, 371]
    time_stamp = [1386, 442]
    chatroom_switch_arrow = [1329, 370] 
    chatroom_option_all = [1174, 520]

    pyautogui.click(any_YT_position)
    time.sleep(round(random.uniform(1, 2), 2))

    if game == target[0]: ## 好像只有第一個不會自動載入
        pyautogui.click(play_position)
        time.sleep(round(random.uniform(1, 2), 2))

    start_time = time.time()

    pyautogui.click(setting_position)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(speed)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(def_speed)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(x2_position)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(play_position)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(setting_position)
    time.sleep(round(random.uniform(1, 2), 2)) 

    pyautogui.click(qua_position)
    time.sleep(round(random.uniform(1, 2), 2)) 

    pyautogui.click(qua_scroll_down)
    time.sleep(round(random.uniform(1, 2), 2))
    pyautogui.click(qua_scroll_down)
    time.sleep(round(random.uniform(1, 2), 2))
    pyautogui.click(qua_scroll_down)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(low_144p)
    time.sleep(round(random.uniform(1, 2), 2)) 

    pyautogui.click(chat_setting)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(time_stamp)
    time.sleep(round(random.uniform(1, 2), 2))

    pyautogui.click(chatroom_switch_arrow)
    time.sleep(round(random.uniform(1, 3), 2))

    pyautogui.click(chatroom_option_all)
    time.sleep(round(random.uniform(1, 3), 2))

    history = []
    extracted_data = []
    conti = True

    duration = videosSearch.result()['result'][0]['duration'].split(":")
    hour = int(duration[0])
    min = int(duration[1])
    sec = int(duration[2])

    game_time = (hour * 3600 + min * 60 + sec) / 1.95

    while conti:
        
        ctrl_a()
        ctrl_c()
        content = read_clipboard()[:-2]

        extracted_data = extract_data(content)
        driver.delete_all_cookies()

        play_time = time.time() - start_time

        if play_time > game_time:
            conti = False
    try:
        with open(fr"C:\Users\SL\Desktop\CrowdEye\TVL19_chat\G{game}.json", "w") as outfile:
            json.dump(extracted_data, outfile)
    except:
        with open(f"19_G{game}.json", "w") as outfile:
            json.dump(extracted_data, outfile)
        
    driver.quit()

    time.sleep(10)
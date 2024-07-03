"""
文件路径: auto_uid_grabber/downloader.py
文件名: downloader.py
文件用途: 负责从官方网站下载游戏安装包，并自动下载和设置匹配的 Edge WebDriver
Author: Shuakami <@ByteFreeze>
"""

import os
import re
import time
import json
import pyautogui
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from image_recognition import recognize_image
from config import GAME_DOWNLOAD_URL
from requests.exceptions import RequestException

def get_edge_version():
    computer_name = os.environ.get('COMPUTERNAME', 'SHUAKA')
    if computer_name == 'SHUAKA':
        return '122.0.2365.16'
    else:
        return '126.0.2592.81'

def download_matching_webdriver():
    edge_version = get_edge_version()
    webdriver_url = f"https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win64.zip"
    webdriver_path = os.path.join(os.path.dirname(__file__), "msedgedriver.exe")

    if not os.path.exists(webdriver_path):
        print(f"正在下载 Edge WebDriver (版本 {edge_version})...")
        while True:
            try:
                response = requests.get(webdriver_url, timeout=30)
                response.raise_for_status()
                zip_path = os.path.join(os.path.dirname(__file__), "edgedriver_win64.zip")
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                break
            except RequestException as e:
                print(f"下载失败: {e}. 5秒后重试...")
                time.sleep(5)

        print("正在解压 Edge WebDriver...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(__file__))

        os.remove(zip_path)
        print("Edge WebDriver 设置完成")
    else:
        print("Edge WebDriver 已存在")

    return webdriver_path

def take_screenshot(driver, filename="screenshot.png"):
    driver.save_screenshot(filename)
    return filename

def preprocess_json(json_string):
    # 移除 Markdown 代码块标记和多余的空白字符
    json_string = re.sub(r'^```json\s*|\s*```$', '', json_string, flags=re.MULTILINE)
    return json_string.strip()

def perform_action(action, driver):
    if action['type'] == 'click':
        pyautogui.click(action['x'], action['y'])
    elif action['type'] == 'navigate':
        driver.get(action['url'])
    elif action['type'] == 'wait':
        time.sleep(action['duration'])
    elif action['type'] == 'search':
        driver.get(f"https://www.bing.com/search?q={action['query']}")


def download_game():
    webdriver_path = download_matching_webdriver()

    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    service = Service(webdriver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        driver.get(GAME_DOWNLOAD_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        screenshot_count = 0
        while True:
            screenshot_count += 1
            screenshot = take_screenshot(driver, f"screenshot_{screenshot_count}.png")
            print(f"截图保存为: {screenshot}")

            prompt = ("很抱歉，我看不见。以下是一个名为《绝区零》的游戏官网界面。你拥有完整的操作权限，因为我看不到，所以请你判断如何下载。请尽力解决它，你的目标是成功下载《绝区零》游戏。"
                      "请分析可能的问题并建议下一步操作。你可以选择以下五种操作之一：\n"
                      "1. 点击屏幕上的特定位置（比如下载按钮或者跳转到下载按钮）（提供x和y坐标）\n"
                      "2. 更换网站（给出网址）\n"
                      "3. 等待一段时间（以秒为单位）\n"
                      "4. 使用必应搜索\n"
                      "5. 确认下载完成\n"
                      "请以JSON格式回答，包含'type'、'x'、'y'、'url'、'duration'、'query'或'status'字段。")

            max_retries = 3
            for retry in range(max_retries):
                try:
                    print(f"正在进行图像识别，尝试 {retry + 1}/{max_retries}")
                    response = recognize_image(screenshot, prompt)
                    print(f"图像识别返回: {response}")

                    # 预处理 JSON 字符串
                    processed_response = preprocess_json(response)

                    action = json.loads(processed_response)
                    break
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
                    print(f"原始响应: {response}")
                    if retry < max_retries - 1:
                        print("重试中...")
                        time.sleep(2)
                    else:
                        print("达到最大重试次数，跳过此次操作")
                        action = None
                except Exception as e:
                    print(f"图像识别过程中发生未知错误: {e}")
                    action = None
                    break

            if action is None:
                print("无法获取有效操作，等待10秒后继续...")
                time.sleep(10)
                continue

            print(f"执行操作: {action}")

            if action['type'] == 'confirm':
                if action['status'] == 'completed':
                    print("下载已完成")
                    break
                else:
                    print("下载尚未完成，继续等待...")
                    time.sleep(10)
                    continue

            perform_action(action, driver)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    download_game()
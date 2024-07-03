import os
import random
import threading
import time
import logging
import keyboard
import numpy as np
import pyautogui
import cv2
import requests
import base64
import json
from config import OPENAI_API_KEY, OPENAI_API_URL
import pygetwindow as gw

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("game-main.log"), logging.StreamHandler()])
logging.getLogger().setLevel(logging.NOTSET)

# 设置图片路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist', 'login')

# 获取当前脚本的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"当前脚本所在目录：{script_directory}")

pause_event = threading.Event()


def pause_for_60_seconds():
    logging.info("检测到 Tab+F 组合键，程序暂停 60 秒")
    pause_event.set()
    time.sleep(60)
    pause_event.clear()
    logging.info("暂停结束，程序继续运行")


# 设置键盘监听
keyboard.add_hotkey('tab+f', pause_for_60_seconds)


def ensure_zzz_foreground():
    try:
        windows = gw.getWindowsWithTitle('绝区零')
        if windows:
            window = windows[0]
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)
        else:
            logging.warning("未找到 ZenlessZoneZero.exe 窗口，但将继续执行")
    except Exception as e:
        logging.warning(f"确保窗口在前台时发生错误，但将继续执行: {e}")


def get_image_path(image_name):
    return os.path.join(DIST_DIR, f"{image_name}.png")


def capture_screen():
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(SCRIPT_DIR, "game_full.png")
        screenshot.save(screenshot_path)
        logging.info(f"截图成功,保存至: {screenshot_path}")
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    except Exception as e:
        logging.warning(f"截图时发生错误，但将继续执行: {e}")
        return None


def detect_image(template_path, screenshot, confidence=0.45):
    try:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= confidence:
            return True, max_loc
        return False, None
    except Exception as e:
        logging.warning(f"图像检测时发生错误，但将继续执行: {e}")
        return False, None


def smart_click():
    ensure_zzz_foreground()
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=random.uniform(0.5, 0.8))
            pyautogui.click(screen_width // 2, screen_height // 2)
            logging.info(f"点击屏幕中间：坐标 ({screen_width // 2}, {screen_height // 2})")

            time.sleep(1.5)
            screenshot = capture_screen()
            if screenshot is None:
                continue

            not_open_found, not_open_loc = detect_image(get_image_path('not-open'), screenshot)
            too_many_found, too_many_loc = detect_image(get_image_path('Too-Many-operatios'), screenshot)

            if not_open_found:
                ensure_zzz_foreground()
                logging.info("检测到 not-open")
                cancel_found, cancel_loc = detect_image(get_image_path('cancel'), screenshot)
                if cancel_found:
                    cancel_template = cv2.imread(get_image_path('cancel'), cv2.IMREAD_GRAYSCALE)
                    cancel_center = (
                        cancel_loc[0] + cancel_template.shape[1] // 2, cancel_loc[1] + cancel_template.shape[0] // 2)
                    pyautogui.moveTo(cancel_center[0], cancel_center[1], duration=random.uniform(0.5, 0.8))
                    pyautogui.click(cancel_center[0], cancel_center[1])
                    logging.info(f"点击cancel按钮：坐标 {cancel_center}")
                time.sleep(3.5)
            elif too_many_found:
                ensure_zzz_foreground()
                logging.info("检测到 Too-Many-operatios")
                confirm_found, confirm_loc = detect_image(get_image_path('confirm'), screenshot)
                if confirm_found:
                    confirm_template = cv2.imread(get_image_path('confirm'), cv2.IMREAD_GRAYSCALE)
                    confirm_center = (
                        confirm_loc[0] + confirm_template.shape[1] // 2,
                        confirm_loc[1] + confirm_template.shape[0] // 2)
                    pyautogui.click(confirm_center[0], confirm_center[1])
                    logging.info(f"点击confirm按钮：坐标 {confirm_center}")
                time.sleep(7)
            else:
                logging.info("未检测到 not-open 或 Too-Many-operatios")
                cadpa_found, _ = detect_image(get_image_path('CADPA'), screenshot)
                if not cadpa_found:
                    logging.info("疑似进入游戏")
                    time.sleep(5)
                    start_game_screenshot = pyautogui.screenshot()
                    start_game_screenshot.save(os.path.join(SCRIPT_DIR, "start_game_main.png"))
                    return True  # 返回True表示可能进入了游戏

        except Exception as e:
            logging.warning(f"在 smart_click 中发生错误，但将继续执行: {e}")

        attempts += 1

    logging.info("达到最大尝试次数,退出循环")
    return False


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.warning(f"图像编码时发生错误，但将继续执行: {e}")
        return None


def analyze_game_screen():
    try:
        image_path = os.path.join(SCRIPT_DIR, "start_game_main.png")
        base64_image = encode_image(image_path)
        if base64_image is None:
            return None

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个精确的图像分析助手，专门用于帮助盲人用户分析游戏界面。你的任务是提供准确的信息和坐标，以帮助用户成功进入游戏并获取UID。请记住，这是一个1920x1080分辨率的屏幕。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请分析以下游戏截图，并提供以下信息：\n"
                                    "1. UID：如果可见，请提供准确的UID号码。\n"
                                    "2. 点击坐标：如果需要点击某个按钮或区域，请提供精确的x和y坐标。坐标应在1920x1080的范围内，左上角为(0,0)。\n"
                                    "3. 游戏状态：判断是否已进入游戏主界面。\n"
                                    "4. 操作建议：简要说明下一步应该做什么。\n\n"
                                    "请以JSON格式回答，包含以下字段：\n"
                                    "- 'uid': UID号码（如果找到），否则为null\n"
                                    "- 'click_coordinates': 包含'x'和'y'的对象，表示需要点击的坐标\n"
                                    "- 'message': 简短的操作建议\n"
                                    "- 'in_game': 布尔值，表示是否已进入游戏主界面\n"
                                    "请确保所有坐标都在1920x1080的范围内，并尽可能准确。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1200
        }

        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        logging.warning(f"分析游戏画面时发生错误，但将继续执行: {e}")
        return None


def main():
    while True:
        try:
            if pause_event.is_set():
                time.sleep(1)  # 如果暂停事件被设置，每秒检查一次
                continue

            if smart_click():
                ensure_zzz_foreground()
                logging.info("可能进入游戏,开始分析游戏画面")
                analysis_result = analyze_game_screen()
                if analysis_result is None:
                    logging.warning("无法获取分析结果，重新尝试")
                    continue

                logging.info(f"GPT分析结果: {analysis_result}")

                # 解析 GPT 返回的 JSON 结果
                try:
                    content = analysis_result['choices'][0]['message']['content']
                    # 移除可能的 Markdown 代码块标记
                    content = content.strip('`').strip()
                    if content.startswith('json'):
                        content = content[4:].strip()
                    gpt_response = json.loads(content)
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    logging.warning(f"无法解析 GPT 返回的 JSON 结果: {e}")
                    continue

                uid = gpt_response.get('uid')
                click_coordinates = gpt_response.get('click_coordinates')
                message = gpt_response.get('message')
                in_game = gpt_response.get('in_game')

                if uid:
                    logging.info(f"检测到 UID: {uid}")
                    try:
                        with open("detected_uid.txt", "w") as f:
                            f.write(uid)
                    except Exception as e:
                        logging.warning(f"写入 UID 到文件时发生错误: {e}")

                if click_coordinates:
                    try:
                        x = click_coordinates.get('x')
                        y = click_coordinates.get('y')
                        if x is not None and y is not None:
                            logging.info(f"需要点击的坐标: ({x}, {y})")
                            pyautogui.moveTo(x, y, duration=random.uniform(0.5, 0.8))
                            pyautogui.click(x, y)
                        else:
                            logging.warning("无效的点击坐标")
                    except Exception as e:
                        logging.warning(f"执行点击操作时发生错误: {e}")

                if message:
                    logging.info(f"GPT 消息: {message}")

                if in_game:
                    logging.info("已成功进入游戏主界面")
                    break  # 成功进入游戏，退出主循环
                else:
                    logging.info("尚未进入游戏主界面，继续尝试")
            else:
                logging.info("未能成功进入游戏，重新尝试")
        except KeyboardInterrupt:
            logging.info("检测到 Ctrl+C,程序退出")
            break
        except Exception as e:
            logging.error(f"发生错误，但将继续执行: {e}")

    logging.info("程序结束")


if __name__ == "__main__":
    # 启动键盘监听
    keyboard.hook_key('tab', lambda e: None)  # 防止 Tab 键的默认行为
    keyboard.hook_key('f', lambda e: None)  # 防止 F 键的默认行为

    main()

import os
import random
import time
import logging
import pyautogui
import psutil
import cv2
import pygetwindow as gw
from PIL import ImageGrab
import subprocess
import sys

# 设置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 文件处理器
file_handler = logging.FileHandler("login.log")
file_handler.setFormatter(formatter)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 添加处理器到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 设置图片路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist', 'login')

# 获取当前脚本的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"当前脚本所在目录：{script_directory}")


# 确保绝区零在顶层
def ensure_zzz_foreground():
    try:
        window = gw.getWindowsWithTitle('绝区零')[0]  # 窗口标题包含 '绝区零'
        if window.isMinimized:
            window.restore()  # 如果窗口最小化,则恢复窗口
        if not window.isActive:
            window.activate()  # 如果窗口未激活,则激活窗口
            time.sleep(1)  # 等待窗口激活
        return True
    except IndexError:
        logging.error("未找到 ZenlessZoneZero.exe 窗口")
        return False



def get_image_path(image_name):
    return os.path.join(DIST_DIR, f"{image_name}.png")

def capture_screen():
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(DIST_DIR, "login_full_screenshot.png")
    screenshot.save(screenshot_path, 'PNG')
    return screenshot_path

def detect_image(template_path, screenshot_path, confidence=0.75):
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= confidence:
        return True, max_loc
    return False, None

def click_image(image_name, confidence=0.75):
    image_path = get_image_path(image_name)
    screenshot_path = capture_screen()
    found, position = detect_image(image_path, screenshot_path, confidence)
    if found:
        screen_width, screen_height = pyautogui.size()
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(image_path)

        center_x = position[0] + template.shape[1] // 2
        center_y = position[1] + template.shape[0] // 2

        screen_x = center_x / screenshot.shape[1] * screen_width
        screen_y = center_y / screenshot.shape[0] * screen_height

        logger.info(f"点击 {image_name} - 屏幕坐标: ({screen_x}, {screen_y})")

        pyautogui.moveTo(screen_x, screen_y, duration=0.5)
        pyautogui.click()

        return True
    logger.warning(f"未找到 {image_name}")
    return False

def check_game_process():
    for proc in psutil.process_iter(['name', 'exe', 'pid']):
        if proc.info['name'] == "ZenlessZoneZero.exe":
            try:
                window = pyautogui.getWindowsWithTitle("绝区零")[0]
                logger.info(f"找到游戏进程：{proc.info}")
                return proc.info
            except IndexError:
                pass
    return None

def confirm_agreement():
    # 等待前置缓冲3分钟
    time.sleep(180)
    for _ in range(2):
        if click_image('Game-Agreen-CB') and click_image('acceptCB'):
            logger.info("确认了协议")
            return True
        time.sleep(3)
    logger.warning("未能确认协议")
    return False



def wait_for_login_window():
    for _ in range(10):
        if click_image('login-modal', confidence=0.65):
            logger.info("检测到登录窗口")
            return True
        time.sleep(15)
    logger.error("未检测到登录窗口")
    return False

def realistic_typing(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.1, 0.3))

def login(account, password):
    if click_image('AAP'):
        time.sleep(3)
        if click_image('enter-account'):
            # 先切换ENG输入法
            pyautogui.hotkey('ctrl', 'space')
            realistic_typing(account)
        time.sleep(3)
        if click_image('enter-password'):
            realistic_typing(password)
        time.sleep(2)
        if click_image('check-box') and click_image('confirm-login'):
            logger.info("完成登录操作")
            return True
    logger.error("登录操作失败")
    return False

def check_restart():
    if click_image('restart-game', confidence=0.65):
        logger.info("检测到需要重启游戏")
        click_image('confirm-button')
        return True
    return False


def force_restart_game(game_info):
    if game_info:
        try:
            psutil.Process(game_info['pid']).terminate()
            logger.info(f"终止游戏进程：{game_info['pid']}")
        except psutil.NoSuchProcess:
            logger.warning("游戏进程已经结束")

    time.sleep(5)

    if 'exe' in game_info:
        subprocess.Popen(game_info['exe'])
        logger.info(f"重新启动游戏：{game_info['exe']}")
    else:
        logger.error("无法重启游戏，缺少可执行文件路径")

    time.sleep(10)



def main():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info("等待游戏启动")
            time.sleep(120) # 2分钟

            ensure_zzz_foreground()

            game_info = check_game_process()
            if not game_info:
                logger.error("未找到游戏进程")
                continue

            # 检查并处理游戏重启情况
            for _ in range(15):
                if check_restart():  # 如果检测到重启按钮
                    logger.info("已处理重启")
                    break
                time.sleep(4)  # 每次检测间隔4秒
            else:
                logger.error("15次检测后没有发现重启按钮，继续其他流程")

            confirm_agreement()

            time.sleep(28)
            if not wait_for_login_window():
                logger.error("未能检测到登录窗口，重启游戏")
                force_restart_game(game_info)
                continue
            ensure_zzz_foreground()
            try:
                with open(os.path.join(SCRIPT_DIR, 'password', 'default.txt'), 'r') as f:
                    account, password = f.read().strip().split(',')
            except Exception as e:
                logger.error(f"读取账号密码失败: {e}")
                return

            if not login(account, password):
                logger.error("登录失败")
                game_info = check_game_process()
                force_restart_game(game_info)
                continue

            time.sleep(60)
            ensure_zzz_foreground()
            if check_restart():
                time.sleep(30)
                if click_image('start_game'):
                    logger.info("成功进入游戏")
                    logger.info("登录流程完成")
                    time.sleep(3)
                    # 启动安装脚本
                    subprocess.run([sys.executable, os.path.join(script_directory, "game-main.py")])
                    logging.info("uid脚本已正常启动——真是一场酣畅淋漓的接力啊~")
                    return
                else:
                    logger.error("未能成功进入游戏")
                    continue

            logger.info("登录流程完成")
            time.sleep(3)
            # 启动安装脚本
            subprocess.run([sys.executable, os.path.join(script_directory, "game-main.py")])
            logging.info("uid脚本已正常启动——真是一场酣畅淋漓的接力啊~")
            return

        except Exception as e:
            logger.error(f"发生错误: {e}")
            if attempt < max_retries - 1:
                logger.info("重试登录流程")
                game_info = check_game_process()
                force_restart_game(game_info)
            else:
                logger.error("达到最大重试次数，退出")

if __name__ == "__main__":
    main()
import re
import cv2
import time
import logging
import numpy as np
import psutil
from PIL import Image, ImageGrab
import pyautogui
import pygetwindow as gw
import os
import sys
import pytesseract
from logging.handlers import RotatingFileHandler
import subprocess

# 导入PaddleOCR
from paddleocr import PaddleOCR

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 设置图片路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist', 'install')
LOG_FILE = os.path.join(SCRIPT_DIR, 'install.log')

# 创建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 创建RotatingFileHandler
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
file_handler.setFormatter(formatter)

# 创建StreamHandler（用于控制台输出）
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 将handlers添加到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 移除所有现有的handlers（以防万一）
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 重新添加handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(console_handler)

# 获取当前脚本的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"当前脚本所在目录：{script_directory}")



def get_image_path(image_name):
    return os.path.join(DIST_DIR, f"{image_name}.png")

def find_and_start_hyp():
    # 先查 hyp.exe 是否已经在运行
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == "hyp.exe":
            logging.info("发现正在运行的 hyp.exe，不做操作")
            return True

    launcher_paths = [
        r"E:\miHoYo Launcher\launcher.exe",
        r"C:\Program Files\miHoYo Launcher\launcher.exe"
    ]

    for path in launcher_paths:
        if os.path.exists(path):
            os.startfile(path)
            logging.info(f"启动 launcher.exe 在路径: {path}")
            time.sleep(3)  # 给予更多时间让 launcher.exe 启动并可能启动 hyp.exe

            # 检查 hyp.exe 是否已经启动
            for _ in range(6):  # 最多等待 30 秒
                if any(proc.info['name'].lower() == "hyp.exe" for proc in psutil.process_iter(['name'])):
                    logging.info("hyp.exe 已成功启动")
                    return True
                time.sleep(5)

            logging.warning("launcher.exe 已启动，但未检测到 hyp.exe")
            return False

    logging.warning("未找到 launcher.exe")
    return False


def capture_screen():
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(DIST_DIR, "install_full_screenshot.png")
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
        pyautogui.click(position[0] + 10, position[1] + 10)
        logging.info(f"点击了 {image_name}")
        return True
    logging.warning(f"未找到 {image_name}")
    return False


def handle_disk_space_error():
    if click_image('error-no-disk-space'):
        logging.info("检测到磁盘空间不足错误，尝试更改安装目录")
        if click_image('change-install-dir'):
            if click_image('C-drive-win10') or click_image('C-drive-win11'):
                if click_image('select-folder') and click_image('install'):
                    logging.info("成功更改安装目录并点击安装")
                    return True
            logging.error("未能成功点击C盘图标")
            return False
        else:
            logging.error("更改安装目录过程中出错")
            return False
    return False


def parse_download_info(text):
    # 初始化信息为未知
    progress = "未知"
    speed = "未知"
    time_left = "未知"

    # 匹配下载进度
    progress_match = re.search(r'下载中\s+(\d+)', text)
    if progress_match:
        progress = progress_match.group(1) + "%"

    # 匹配下载速度
    speed_match = re.search(r'(\d+\.?\d*\s*[KMG]?B/s)', text)
    if speed_match:
        speed = speed_match.group(1)

    # 匹配剩余时间
    time_match = re.search(r'(\d{1,3}:\d{2}:\d{2})', text)
    if time_match:
        time_left = time_match.group(1)

    return progress, speed, time_left


def ensure_hyp_foreground():
    try:
        window = gw.getWindowsWithTitle('米哈游启动器')[0]
        if window.isMinimized:
            window.restore()
        if not window.isActive:
            window.activate()
        time.sleep(1)  # 等待窗口激活
        return True
    except IndexError:
        logging.error("未找到 hyp.exe 窗口")
        return False


def terminate_hyp():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == "hyp.exe":
            proc.terminate()
            logging.info("已终止 hyp.exe 进程")
            time.sleep(2)  # 等待进程完全结束
            return True
    logging.warning("未找到正在运行的 hyp.exe 进程")
    return False


def get_button_region(screenshot, start_game=False):
    if start_game:
        template_path = os.path.join(DIST_DIR, "start_game.png")
    else:
        template_path = os.path.join(DIST_DIR, "installing.png")

    if not os.path.exists(template_path):
        logging.error(f"Template file not found: {template_path}")
        return None

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logging.error(f"Failed to read template image: {template_path}")
        return None

    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.65:
        top_left = max_loc
        w, h = template.shape[::-1]
        button_center = (top_left[0] + w // 2, top_left[1] + h // 2)

        return button_center  # 返回按钮中心位置，用于点击
    else:
        logging.warning("Template not found in the screenshot")
        return None


def monitor_installation():
    while True:
        logging.info("开始新一轮监控...")
        ensure_hyp_foreground()
        screenshot = ImageGrab.grab()
        logging.info("已捕获屏幕截图")

        try:
            button_pos = get_button_region(screenshot)
            if button_pos:
                logging.info("成功获取按钮区域位置")
                button_image = screenshot.crop(
                    (button_pos[0] - 50, button_pos[1] - 20, button_pos[0] + 50, button_pos[1] + 20))
                button_image_np = np.array(button_image)

                # 高度，宽度，通道
                if len(button_image_np.shape) == 2:
                    button_image_np = cv2.cvtColor(button_image_np, cv2.COLOR_GRAY2RGB)

                result = ocr.ocr(button_image_np, cls=True)
                logging.info(f"Raw OCR result: {result}")

                if result:
                    text = ' '.join([item[1][0] for item in result[0] if isinstance(item, list) and len(item) > 1])
                    logging.info(f"Extracted text: {text}")

                    if "下载中" in text or "安装中" in text:
                        progress, speed, time_left = parse_download_info(text)
                        logging.info(f"下载/安装中 - 当前进度 {progress} - 剩余时间 {time_left} - 速度 {speed}")
                        time.sleep(20)  # 每20秒检查一次
                    elif "开始游戏" in text:
                        logging.info("安装完成，监控结束。")
                        break
                    else:
                        logging.warning("未识别到已知状态，当前文本: {text}，10秒后重新检查")
                        time.sleep(10)
                else:
                    logging.warning("OCR 未识别到任何有效文本。")
                    time.sleep(10)
            else:
                logging.warning("按钮区域未在截图中找到。")
                start_game_path = os.path.join(DIST_DIR, "start_game.png")
                start_game_template = cv2.imread(start_game_path)
                if start_game_template is not None:
                    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    result = cv2.matchTemplate(screenshot_cv, start_game_template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val >= 0.93:
                        logging.info("匹配到开始游戏按钮，游戏安装完成。")
                        logging.info("绝区零...启动！")

                        button_center_x, button_center_y = max_loc[0] + start_game_template.shape[1] // 2, max_loc[1] + \
                                                           start_game_template.shape[0] // 2
                        pyautogui.click(button_center_x, button_center_y)
                        subprocess.run([sys.executable, os.path.join(script_directory, "login.py")])
                        logging.info("登录脚本已正常启动——真是一场酣畅淋漓的接力啊")
                        break
                    else:
                        logging.warning("未匹配到开始游戏按钮，10秒后重新检查。")
                        # 检测鼠标是否悬停在显示进度的区域
                        hover_paused_path = os.path.join(DIST_DIR, "hover-paused.png")
                        hover_paused_found, _ = detect_image(hover_paused_path, capture_screen())
                        if hover_paused_found:
                            logging.info("检测到鼠标悬停在显示进度区域，尝试移开鼠标...")
                            pyautogui.moveTo(100, 100)  # 将鼠标移动到屏幕左上角

                        # 检测是否出现 "download-paused" 图像
                        download_paused_path = os.path.join(DIST_DIR, "download-paused.png")
                        download_paused_found, position = detect_image(download_paused_path, capture_screen())
                        if download_paused_found:
                            logging.warning("检测到下载暂停，尝试点击继续...")
                            if position:
                                click_x, click_y = position
                                pyautogui.moveTo(click_x, click_y, duration=0.5)  # 慢慢移动到目标位置
                                pyautogui.click()

                        if position:
                            x, y = position
                            screen_width, screen_height = pyautogui.size()
                            click_x = int(x * screen_width)
                            click_y = int(y * screen_height)

                            pyautogui.moveTo(click_x, click_y, duration=0.5)  # 慢慢移动到目标位置
                            pyautogui.click()
                            logging.info(f"点击了暂停下载按钮,坐标为 ({click_x}, {click_y})")
                        time.sleep(10)
                else:
                    logging.error(f"开始游戏模板图像读取失败: {start_game_path}")
                    time.sleep(10)


        except Exception as e:
            logging.error(f"监控安装过程时发生错误: {str(e)}", exc_info=True)
            time.sleep(5)  # 发生错误时等待5秒后重试


def restart_script():
    # 结束这个脚本，启动新脚本
    logging.info("重启安装脚本_OCR...")
    subprocess.run([sys.executable, os.path.join(script_directory, "start_ocr.py")])
    return True


def attempt_install():
    logging.warning("未匹配到开始游戏按钮，10秒后重新检查。")
    # 检测鼠标是否悬停在显示进度的区域
    hover_paused_path = os.path.join(DIST_DIR, "hover-paused.png")
    hover_paused_found, _ = detect_image(hover_paused_path, capture_screen())
    if hover_paused_found:
        logging.info("检测到鼠标悬停在显示进度区域，尝试移开鼠标...")
        pyautogui.moveTo(100, 100)  # 将鼠标移动到屏幕左上角
        return True
    elif click_image('install'):
        logging.info("找到并点击了安装按钮")
        time.sleep(5)  # 等待安装开始
        return True
    elif click_image('get-games'):
        logging.info("找到并点击了获取游戏按钮")
        time.sleep(5)  # 等待界面更新
        # 检测并处理空间不足问题
        if handle_disk_space_error():
            logging.info("处理了磁盘空间不足的问题")
            time.sleep(5)  # 等待界面更新
            # 在处理空间不足后重新尝试点击安装按钮
            if click_image('install'):
                logging.info("再次找到并点击了安装按钮")
                time.sleep(5)  # 等待安装开始
                return True
    elif handle_disk_space_error():
        logging.info("处理了磁盘空间不足的问题")
        time.sleep(5)  # 等待安装开始
        return True
    else:
        # 检测 re-download.png, installing.png, download-paused.png 和 start_game.png
        re_download_path = os.path.join(DIST_DIR, "re-download.png")
        installing_path = os.path.join(DIST_DIR, "installing.png")
        download_paused_path = os.path.join(DIST_DIR, "download-paused.png")
        start_game_path = os.path.join(DIST_DIR, "start_game.png")
        screenshot_path = capture_screen()

        re_download_found, re_download_pos = detect_image(re_download_path, screenshot_path)
        installing_found, installing_pos = detect_image(installing_path, screenshot_path, confidence=0.7)
        download_paused_found, download_paused_pos = detect_image(download_paused_path, screenshot_path)
        start_game_found, start_game_pos = detect_image(start_game_path, screenshot_path, confidence=0.95)

        if installing_found:
            logging.info("检测到正在下载/安装，跳转到监控步骤")
            return True
        elif re_download_found:
            logging.info("已恢复下载...")
            pyautogui.click(re_download_pos[0] + 10, re_download_pos[1] + 10)
            time.sleep(5)  # 等待下载开始
            return True
        elif download_paused_found:
            logging.info("检测到下载暂停，尝试恢复下载...")
            pyautogui.click(download_paused_pos[0] + 10, download_paused_pos[1] + 10)
            time.sleep(5)  # 等待下载恢复
            return True
        elif start_game_found:
            logging.info("检测到开始游戏按钮，尝试点击...")
            pyautogui.click(start_game_pos[0] + 10, start_game_pos[1] + 10)
            logging.info("游戏启动成功，绝区零..启动！")
            subprocess.run([sys.executable, os.path.join(script_directory, "login.py")])
            logging.info("登录脚本已正常启动——真是一场酣畅淋漓的接力啊")
            return True

    return False


def main():
    max_attempts = 505 # 大概是125分钟
    attempt = 0

    while True:
        try:
            ensure_hyp_foreground()
            find_and_start_hyp()
            time.sleep(5)
            if attempt_install():
                monitor_installation()
                return  # 成功安装，退出函数

            logging.warning("未能安装，尝试点击'获取游戏'按钮")
            if click_image('get-games'):
                logging.info("成功点击'获取游戏'按钮，立即尝试安装")
                time.sleep(5)  # 等待界面更新
                for _ in range(3):
                    if attempt_install():
                        monitor_installation()
                        return
                    time.sleep(2)

            # logging.error("多次尝试后仍未能安装，重启脚本")
            # restart_script()

        except Exception as e:
            logging.error(f"发生错误: {e}")
            time.sleep(15)
            attempt += 1
            if attempt >= max_attempts:
                logging.critical(f"脚本执行了 {max_attempts} 次仍然失败，重启脚本")
                terminate_hyp()
                restart_script()
            else:
                logging.info(f"5秒后进行第 {attempt + 1} 次尝试")
                time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("用户中断了脚本执行")
    except Exception as e:
        logging.critical(f"发生了未预期的错误: {e}")
        restart_script()

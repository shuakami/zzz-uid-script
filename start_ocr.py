import sys
import subprocess
import os
import atexit
import importlib.util
import urllib.request


def on_exit():
    input("Press Enter to continue...")


atexit.register(on_exit)

# 全局变量存储网络状态
network_is_ok = False


def check_internet():
    global network_is_ok
    urls = [
        'https://cn.bing.com',
        'https://www.gov.cn',
    ]
    success_count = 0
    for url in urls:
        try:
            urllib.request.urlopen(url, timeout=0.5)
            success_count += 1
            if success_count >= 1:  # 只要有1个成功即认为网络正常
                network_is_ok = True
                print("CDN已链接->网络正常")
                return
        except:
            continue
    print("网络连接异常，请检查您的网络设置")
    network_is_ok = False


def clear_pip_cache():
    subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], check=True)


mirrors = [
    "https://mirrors.ustc.edu.cn/pypi/web/simple",
    "https://mirrors.ustc.edu.cn/simple",
    "https://mirrors.aliyun.com/pypi/simple",
    "https://mirrors.cloud.tencent.com/pypi/simple",
]


def install(package, mirror_index=0):
    if mirror_index >= len(mirrors):
        print(f"所有镜像源都尝试失败，尝试离线安装...")
        return install_offline(package)

    cmd = [sys.executable, "-m", "pip", "install", "-i", mirrors[mirror_index], package]

    try:
        print(f"正在从 {mirrors[mirror_index]} 安装 {package}...")
        subprocess.check_call(cmd, timeout=180)  # 3分钟超时
        print(f"{package} 安装完成")
        return True
    except subprocess.TimeoutExpired:
        print(f"从 {mirrors[mirror_index]} 安装 {package} 超时")
    except subprocess.CalledProcessError as e:
        print(f"从 {mirrors[mirror_index]} 安装 {package} 失败: {e}")

    return install(package, mirror_index + 1)


def install_offline(package):
    offline_path = f"./offline_packages/{package}.whl"
    if os.path.exists(offline_path):
        cmd = [sys.executable, "-m", "pip", "install", offline_path]
        try:
            subprocess.check_call(cmd)
            print(f"{package} 已通过离线包安装")
            return True
        except subprocess.CalledProcessError:
            print(f"离线安装 {package} 失败")
    return False


required_packages = [
    'opencv-python', 'psutil', 'pillow', 'pyautogui', 'pygetwindow', 'pytesseract', 'paddlepaddle', 'numpy', 'paddle','keyboard'
]

# 特殊导入包名
package_name_mapping = {
    'opencv-python': 'cv2',
    'pillow': 'PIL',
    'paddlepaddle': 'paddle',
}


def is_package_installed(package_name):
    module_name = package_name_mapping.get(package_name, package_name)
    try:
        importlib.import_module(module_name.replace('-', '_').split('.')[0])
        return True
    except ImportError:
        return False


def check_and_install_packages():
    check_internet()  # 仅在开始时检查网络一次
    for package in required_packages:
        if not is_package_installed(package):
            print(f"{package} 未安装，尝试安装...")
            if not network_is_ok:
                print("网络连接失败，尝试离线安装...")
                if not install_offline(package):
                    print(f"无法安装 {package}，请检查网络连接后重试")
                    return False
            else:
                clear_pip_cache()
                if not install(package):
                    return False
        else:
            print(f"{package} 已安装")
    return True


print("检查并安装所需的包...")
check_and_install_packages()
print("所有必要的包已安装")
print("")
print("--------------------------------")
print("ZZZ _ ZZZ")
print("The ZZZ Game UID Script")
print("Version: 1.0.0 | Pre-Alpha | Powered by Shuakami<速冻饺子>")
print("免责声明：")
print(
    "本脚本旨在为游戏玩家提供方便，仅供学习和研究之用。开发者不承担由于使用此脚本而导致的任何直接或间接损失责任。用户在使用本脚本时，应自行承担所有风险。不得将本脚本用于任何非法目的，否则后果自负。")
print("Disclaimer:")
print("This script is intended to provide convenience for gamers and is for educational and research purposes only. "
      "The developer assumes no liability for any direct or indirect damages resulting from the use of this script. "
      "Users should assume all risks associated with its use. This script must not be used for any illegal purposes, "
      "and any consequences are the sole responsibility of the user.")
print("--------------------------------")
print("")

import cv2
import time
import psutil
import logging
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
from logging.handlers import RotatingFileHandler

# 等待4秒给用户阅读之前的输出
time.sleep(4)

# 获取当前脚本的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"当前脚本所在目录：{script_directory}")

# 设置图片路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist')
LOG_FILE = os.path.join(SCRIPT_DIR, 'game_login.log')

# 设置日志的配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建文件处理器，用于写入日志文件
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 添加处理器到日志记录器
logger.addHandler(file_handler)


def get_image_path(image_name):
    return os.path.join(DIST_DIR, image_name)


# 确保 hyp.exe 在顶层
def ensure_hyp_foreground():
    try:
        window = gw.getWindowsWithTitle('米哈游启动器')[0]  # 窗口标题包含 '米哈游启动器'
        if window.isMinimized:
            window.restore()  # 如果窗口最小化,则恢复窗口
        if not window.isActive:
            window.activate()  # 如果窗口未激活,则激活窗口
            time.sleep(1)  # 等待窗口激活
        return True
    except IndexError:
        logging.error("未找到 hyp.exe 窗口")
        return False


def find_and_start_hyp():
    # 先查 hyp.exe 是否已经在运行
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == "hyp.exe":
            logging.info("发现正在运行的 hyp.exe，尝试结束进程")
            proc.terminate()
            time.sleep(2)  # 等待进程完全结束
            break

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


def find_hyp_exe():
    try:
        for proc in psutil.process_iter(['name', 'exe']):
            if proc.info['name'].lower() == "hyp.exe":
                file_path = proc.info['exe']
                logging.info(f"找到 hyp.exe 在路径: {file_path}")
                return True
        logging.warning("未找到 hyp.exe 进程")
        return False
    except Exception as e:
        logging.error(f"查找 hyp.exe 时出错: {e}")
        return False


def capture_hyp_window():
    try:
        screenshot = ImageGrab.grab()  # 无参数调用来捕获全屏幕
        screenshot_path = os.path.join(DIST_DIR, "full_screenshot.png")

        # 如果目录不存在,则创建目录
        os.makedirs(DIST_DIR, exist_ok=True)

        # 保存截图为 PNG 文件
        screenshot.save(screenshot_path, 'PNG')
        logging.info(f"全屏截图已保存: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logging.error(f"截取全屏幕时出错: {e}")
        return None


def detect_image(template_path, screenshot_path, confidence=0.6):
    try:
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)

        if screenshot is None or template is None:
            logging.error(f"无法读取图像: {screenshot_path} 或 {template_path}")
            return False, None

        # 使用模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            logging.info(f"找到图像 {os.path.basename(template_path)} 在位置 {max_loc}")
            return True, max_loc
        else:
            logging.warning(f"未找到图像 {os.path.basename(template_path)}")
            return False, None
    except Exception as e:
        logging.error(f"检测图像时出错: {e}")
        return False, None


def click_image(image_path, screenshot_path, clicks=1, interval=0.25, duration=0.25, confidence=0.5):
    logging.info(f"屏幕分辨率: {pyautogui.size()}")
    logging.info(f"鼠标初始位置: {pyautogui.position()}")

    try:
        found, position = detect_image(image_path, screenshot_path, confidence)
        if found:
            template = cv2.imread(image_path)
            screen_width, screen_height = pyautogui.size()

            # 读取截图并获取其尺寸
            screenshot = cv2.imread(screenshot_path)
            screenshot_height, screenshot_width = screenshot.shape[:2]

            # 计算相对位置
            relative_x = int((position[0] + template.shape[1] // 2) / screenshot_width * screen_width)
            relative_y = int((position[1] + template.shape[0] // 2) / screenshot_height * screen_height)

            try:
                logging.info(f"尝试点击图像 {os.path.basename(image_path)} 在相对位置 ({relative_x}, {relative_y})")
                pyautogui.moveTo(relative_x, relative_y, duration=0.2)  # 移动鼠标到指定位置
                time.sleep(0.3)  # 让鼠标在点击位置停留一段时间

                pyautogui.click(clicks=clicks, interval=interval, duration=duration)
                logging.info(f"点击了图像 {os.path.basename(image_path)} 在相对位置 ({relative_x}, {relative_y})")
                logging.info(f"结束后鼠标位置: {pyautogui.position()}")
                return True
            except Exception as e:
                logging.error(f"点击图像时出错: {e}")
                return False
        else:
            return False
    except Exception as e:
        logging.error(f"检测图像时出错: {e}")
        return False


def main():
    max_attempts = 5  # 最大尝试次数
    attempt = 0  # 当前尝试次数

    while True:  # 无限循环，直到成功或手动中断
        try:
            logging.info(f"开始第 {attempt + 1} 次尝试")

            if not find_hyp_exe():
                logging.warning("未找到正在运行的 hyp.exe")
                restart_hyp()

            steps = [
                ('button_cut', '开启选择按钮', 2),
                ('cut_zzz_background', '绝区零图标', 2),
                ('start_zzz_none', '预约页面', 0),
            ]

            for image, desc, delay in steps:
                if not execute_step(image, desc, delay):
                    raise Exception(f"步骤 '{desc}' 失败")

            # 特殊处理"立即预约按钮"步骤
            if not execute_reservation_step():
                raise Exception("立即预约按钮步骤失败")

            logging.info("脚本执行完成")
            return  # 成功执行完所有步骤，退出函数

        except Exception as e:
            logging.error(f"脚本执行过程中发生错误: {e}")
            attempt += 1
            if attempt >= max_attempts:
                logging.critical(f"脚本执行了 {max_attempts} 次仍然失败")
                restart_script()
            else:
                find_and_start_hyp()
                ensure_hyp_foreground()
                logging.info(f"已经重启，等待 3 秒后重试...")
                time.sleep(3)
                ensure_hyp_foreground()


def restart_hyp():
    logging.info("尝试重启 hyp.exe")
    find_and_start_hyp()
    ensure_hyp_foreground()

    if not find_and_start_hyp():
        logging.error("未能找到并启动 hyp.exe")
        raise Exception("无法启动 hyp.exe")


def execute_step(image, desc, delay):
    image_path = get_image_path(f'{image}.png')
    for step_attempt in range(3):  # 每个步骤最多尝试3次
        ensure_hyp_foreground()  # 确保 HYP 窗口在前台
        screenshot_path = capture_hyp_window()
        if not screenshot_path:
            logging.error(f"未能截取 HYP 窗口,{desc}步骤失败")
            continue

        if click_image(image_path, screenshot_path):
            logging.info(f"点击了{desc}")
            time.sleep(delay)  # 等待界面变化
            return True
    return False


def execute_reservation_step():
    reservation_attempts = 0
    while reservation_attempts < 3:
        ensure_hyp_foreground()
        screenshot_path = capture_hyp_window()
        if not screenshot_path:
            logging.error("未能截取 HYP 窗口")
            reservation_attempts += 1
            continue

        start_zzz_none_path = get_image_path('start_zzz_none.png')
        start_zzz_button_none_path = get_image_path('start_zzz_button_none.png')

        if detect_image(start_zzz_none_path, screenshot_path)[0]:
            if detect_image(start_zzz_button_none_path, screenshot_path)[0]:
                if click_image(start_zzz_button_none_path, screenshot_path):
                    logging.info("点击了立即预约按钮")
                    time.sleep(3)
                    # 启动安装脚本
                    subprocess.run([sys.executable, os.path.join(script_directory, "start_install.py")])
                    logging.info("安装脚本已正常启动——真是一场酣畅淋漓的接力啊~")
                    return True
            else:
                logging.warning("预约页面上没有立即预约按钮")
                return False
        else:
            logging.warning("未匹配到预约页面，尝试重启 hyp")
            find_and_start_hyp()
            ensure_hyp_foreground()
            time.sleep(3)

        reservation_attempts += 1

    return False


def restart_script():
    logging.critical("重启脚本...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("用户中断了脚本执行")
    except Exception as e:
        logging.critical(f"发生了未预期的错误: {e}")
        restart_script()

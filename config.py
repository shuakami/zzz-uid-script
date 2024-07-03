"""
文件路径: auto_uid_grabber/config.py
文件名: config.py
文件用途: 存储配置信息,如API密钥、URL等
Author: Shuakami <@ByteFreeze>
"""

# OpenAI API配置
OPENAI_API_KEY = "your_openai_api_key"  # 替换为你的OpenAI API密钥
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"  # 使用官方的API URL

# 其他配置
GAME_DOWNLOAD_URL = "https://example.com/game_download_url"  # 替换为实际的游戏下载URL
INSTALL_PATH = "C:/Program Files/YourGame"  # 替换为你希望安装游戏的路径

# 日志配置
LOG_FILE = "auto_uid_grabber.log"
LOG_LEVEL = "INFO"
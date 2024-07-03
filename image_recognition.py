"""
文件路径: auto_uid_grabber/image_recognition.py
文件名: image_recognition.py
文件用途: 使用OpenAI API进行图像识别，识别界面元素
Author: Shuakami <@ByteFreeze>
"""

import base64
import openai
from config import OPENAI_API_KEY

# 设置 OpenAI API 密钥
openai.api_key = OPENAI_API_KEY

def encode_image(image_path):
    """
    将图像文件编码为base64字符串
    :param image_path: 图像文件路径
    :return: base64编码的字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def recognize_image(image_path, prompt):
    """
    使用OpenAI API识别图像中的界面元素
    :param image_path: 图像文件路径
    :param prompt: 识别提示
    :return: API返回的识别结果
    """
    base64_image = encode_image(image_path)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

if __name__ == "__main__":
    # 测试代码
    test_image_path = "path/to/your/test/image.jpg"
    test_prompt = "识别这个图像中的界面元素，特别是登录框和按钮的位置"
    result = recognize_image(test_image_path, test_prompt)
    print(result)
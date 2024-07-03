import os
import requests
import zipfile
import subprocess
import time


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"当前脚本所在目录:{script_directory}")

    try:
        # 下载和解压缩
        url = "https://github.com/shuakami/zzz-uid-script/releases/download/v1.0.0/zzz-uid-script-v1.0.0.zip"
        zip_path = os.path.join(script_directory, "temp.zip")
        print("开始下载文件...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("文件下载完成。")

        extract_path = os.path.join(script_directory, "zzz")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(zip_path)
        print(f"解压完成,解压至目录 {extract_path}")

        # 执行子程序
        ocr_script = os.path.join(extract_path, "start_ocr.py")
        process = subprocess.Popen(['python', ocr_script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            if process.poll() is not None:
                break

        print("OCR脚本执行完毕。")

    except Exception as e:
        print(f"发生错误:{e}")


if __name__ == "__main__":
    main()
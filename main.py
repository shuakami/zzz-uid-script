import os
import sys
import time
import subprocess
import traceback


def ensure_requests_installed():
    try:
        import requests
    except ImportError:
        print("requests not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "requests"])
    finally:
        import requests
    return requests


requests = ensure_requests_installed()


def install_requirements():
    try:
        url = "https://github.com/shuakami/zzz-uid-script/releases/download/v1.0.0/pip_install.txt"
        response = requests.get(url)
        packages = response.text.strip().split(',')
        for package in packages:
            if package.strip() != "requests":  # Skip requests as we've already handled it
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                     package.strip()])
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return False
    return True


def download_and_run_script():
    try:
        url = "https://github.com/shuakami/zzz-uid-script/releases/download/v1.0.0/main_zzz_downloadpy_cdn_sdjz_wiki_pr.py"
        response = requests.get(url)
        script_content = response.text
        script_path = "main_zzz_downloadpy_cdn_sdjz_wiki.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        subprocess.run([sys.executable, script_path], check=True)
    except Exception as e:
        print(f"Error downloading or running script: {e}")
        return False
    return True


def fix_script():
    try:
        print("Script fixing functionality is not available in the open-source version.")
        return False
    except Exception as e:
        print(f"Error fixing script: {e}")
        return False


def main():
    while True:
        try:
            if not install_requirements():
                raise Exception("Failed to install requirements")
            if not download_and_run_script():
                raise Exception("Failed to download or run script")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    main()

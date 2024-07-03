# 设置字符编码为UTF-8以支持中文
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置任务触发的时间
$triggerTime = Get-Date -Year 2024 -Month 7 -Day 4 -Hour 7 -Minute 0 -Second 30
Write-Host "Trigger set for: $triggerTime"

# 创建任务触发器
$trigger = New-ScheduledTaskTrigger -Once -At $triggerTime

# 获取当前用户的用户名路径
$userProfilePath = [Environment]::GetFolderPath("UserProfile")

# 构建Python执行路径和工作目录路径
$pythonExecPath = "C:\Program Files\Python311\python.exe"
$workingDirectory = "$userProfilePath\zzz"

# 创建工作目录
New-Item -ItemType Directory -Force -Path $workingDirectory

# 创建main.py文件
$mainPyContent = @"
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
"@

Set-Content -Path "$workingDirectory\main.py" -Value $mainPyContent

# 创建任务操作，执行 Python 脚本
$action = New-ScheduledTaskAction -Execute $pythonExecPath -Argument "$workingDirectory\main.py" -WorkingDirectory $workingDirectory

# 创建任务设置
$settings = New-ScheduledTaskSettingsSet -WakeToRun
Write-Host "Task settings initialized with wake to run."

try {
    # 注册计划任务
    $task = Register-ScheduledTask -TaskName "RunPythonScriptOnJuly4" -Trigger $trigger -Action $action -User "SYSTEM" -Settings $settings -RunLevel Highest -Force
    Write-Host "Task scheduled successfully for July 4th, 2024, at 7:00:30 AM"
    Write-Host "Task Name: $($task.TaskName)"
    Write-Host "Next Run Time: $($task.NextRunTime)"
    Write-Host "Task State: $($task.State)"
}
catch {
    Write-Host "Error occurred: $_"
}

# 检查任务是否存在
if (Get-ScheduledTask -TaskName "RunPythonScriptOnJuly4" -ErrorAction SilentlyContinue) {
    Write-Host "Task exists and is ready."
} else {
    Write-Host "Task does not exist. Check for errors in task creation."
}
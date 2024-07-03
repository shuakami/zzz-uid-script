# 设置字符编码为UTF-8以支持中文
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 定义Python安装包的URL
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
$installerName = "python-3.11.0-amd64.exe"
$installerPath = "$env:TEMP\$installerName"

# 下载Python安装器
Write-Host "Initiating download of Python 3.11 installer from $pythonInstallerUrl..."
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

# 检查下载是否成功
if (Test-Path $installerPath) {
    Write-Host "Download of Python installer completed successfully."
} else {
    Write-Host "Download failed: Installer file not found at $installerPath. Please check the URL or network connectivity."
    exit
}

# 安装Python并添加到PATH
Write-Host "Starting installation of Python 3.11..."
$installArgs = "/quiet InstallAllUsers=1 PrependPath=1"
Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -NoNewWindow

# 验证安装
$pythonExecPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (Test-Path $pythonExecPath) {
    Write-Host "Python 3.11 has been installed successfully and is located at $pythonExecPath"
    # 打开一个新的CMD窗口执行Python版本检查
    Start-Process cmd -ArgumentList "/c echo Testing Python Installation... && python --version && echo Press any key to exit... && pause" -NoNewWindow
} else {
    Write-Host "Installation verification failed: Python executable not found at $pythonExecPath. Check installation logs and permissions."
    exit
}

Write-Host "Python installation script executed successfully. - Shuakami<ByteFreeze>"

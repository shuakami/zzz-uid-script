# 设置字符编码为UTF-8以支持中文
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 常见的Python安装路径
$commonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python",   # 通常的用户级安装路径
    "$env:PROGRAMFILES\Python",            # 通常的系统级安装路径
    "$env:PROGRAMFILES (x86)\Python"       # 可能的32位Python在64位系统上的安装路径
)

# 搜索Python可执行文件
function Find-Python {
    foreach ($path in $commonPaths) {
        $pythonExes = Get-ChildItem -Path $path -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue
        foreach ($exe in $pythonExes) {
            Write-Host "找到Python可执行文件：$($exe.FullName)"
        }
    }
}

# 在常见路径中搜索
Find-Python

# 如果常见路径中没有找到，进行全盘搜索
if ((Get-ChildItem -Path $commonPaths -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue).Count -eq 0) {
    Write-Host "在常见路径中没有找到Python，开始全盘搜索，这可能需要一些时间..."
    $allPythonExes = Get-ChildItem -Path "C:\" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue
    foreach ($exe in $allPythonExes) {
        Write-Host "找到Python可执行文件：$($exe.FullName)"
    }
}

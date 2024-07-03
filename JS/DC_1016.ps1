# 设置输出编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 函数：获取屏幕信息
function Get-ScreenInfo {
    Add-Type -AssemblyName System.Windows.Forms
    $screens = [System.Windows.Forms.Screen]::AllScreens
    $screenInfo = @()
    foreach ($screen in $screens) {
        $screenInfo += [PSCustomObject]@{
            DeviceName = $screen.DeviceName
            Primary = $screen.Primary
            Bounds = $screen.Bounds
            WorkingArea = $screen.WorkingArea
            BitsPerPixel = $screen.BitsPerPixel
        }
    }
    return $screenInfo
}

# 函数：获取显示适配器信息
function Get-DisplayAdapterInfo {
    return Get-WmiObject Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, VideoModeDescription
}

# 函数：获取显示器信息
function Get-MonitorInfo {
    return Get-WmiObject WmiMonitorID -Namespace root\wmi | ForEach-Object {
        [PSCustomObject]@{
            ManufacturerName = (-join [char[]]($_.ManufacturerName -ne 0) -replace '\0').Trim()
            ProductCodeID = (-join [char[]]($_.ProductCodeID -ne 0) -replace '\0').Trim()
            SerialNumberID = (-join [char[]]($_.SerialNumberID -ne 0) -replace '\0').Trim()
            UserFriendlyName = (-join [char[]]($_.UserFriendlyName -ne 0) -replace '\0').Trim()
            YearOfManufacture = $_.YearOfManufacture
        }
    }
}

# 函数：获取 DPI 设置
function Get-DpiSetting {
    Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;

    public class DpiHelper {
        [DllImport("user32.dll")]
        public static extern bool SetProcessDPIAware();

        [DllImport("user32.dll")]
        public static extern int GetDpiForSystem();
    }
"@
    [DpiHelper]::SetProcessDPIAware() | Out-Null
    return [DpiHelper]::GetDpiForSystem()
}

# 函数：获取系统信息
function Get-SystemInfo {
    return Get-WmiObject Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory, NumberOfProcessors, NumberOfLogicalProcessors
}

# 函数：获取处理器信息
function Get-ProcessorInfo {
    return Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, L2CacheSize, L3CacheSize
}

# 函数：获取内存信息
function Get-MemoryInfo {
    return Get-WmiObject Win32_PhysicalMemory | Select-Object Manufacturer, PartNumber, Capacity, Speed
}

# 函数：获取磁盘信息
function Get-DiskInfo {
    return Get-WmiObject Win32_DiskDrive | Select-Object Model, Size, InterfaceType
}

# 函数：获取网络适配器信息
function Get-NetworkAdapterInfo {
    return Get-WmiObject Win32_NetworkAdapter | Where-Object { $_.PhysicalAdapter } | Select-Object Name, AdapterType, MACAddress, Speed
}

# 函数：获取 BIOS 信息
function Get-BiosInfo {
    return Get-WmiObject Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate
}

# 函数：获取操作系统信息
function Get-OSInfo {
    return Get-WmiObject Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture, LastBootUpTime
}

# 函数：获取 DirectX 版本
function Get-DirectXVersion {
    $tempFile = [System.IO.Path]::GetTempFileName()
    try {
        dxdiag /t $tempFile
        Start-Sleep -Seconds 5
        $dxContent = Get-Content $tempFile
        $dxVersion = ($dxContent | Select-String "DirectX Version:").ToString().Split(":")[1].Trim()
        return $dxVersion
    }
    catch {
        return "Unable to retrieve DirectX version"
    }
    finally {
        if (Test-Path $tempFile) {
            Remove-Item $tempFile -Force
        }
    }
}

# 函数：获取声音设备信息
function Get-AudioDevices {
    return Get-WmiObject Win32_SoundDevice | Select-Object Name, Manufacturer, Status
}

# 函数：获取已安装的 .NET Framework 版本
function Get-DotNetVersions {
    $versions = Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -Recurse |
    Get-ItemProperty -Name Version, Release -ErrorAction SilentlyContinue |
    Where-Object { $_.PSChildName -match '^(?!S)\p{L}'} |
    Select-Object @{Name="Version"; Expression={$_.PSChildName}}, Version, Release
    return $versions
}

# 函数：获取启动程序列表
function Get-StartupPrograms {
    $startupFolderPath = [System.Environment]::GetFolderPath('Startup')
    $startupItems = Get-ChildItem -Path $startupFolderPath | Select-Object Name, FullName
    return $startupItems
}

# 函数：获取系统环境变量
function Get-SystemEnvironmentVariables {
    return Get-ChildItem Env: | Select-Object Name, Value
}

# 函数：获取系统服务
function Get-SystemServices {
    return Get-WmiObject Win32_Service | Select-Object Name, DisplayName, State, StartMode
}

# 函数：获取系统字体
function Get-InstalledFonts {
    $fontsFolderPath = [System.Environment]::GetFolderPath('Fonts')
    $fonts = Get-ChildItem -Path $fontsFolderPath | Select-Object Name, FullName
    return $fonts
}

# 函数：获取详细内存信息
function Get-DetailedMemoryInfo {
    $totalMemory = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory
    $availableMemory = (Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory * 1KB
    $usedMemory = $totalMemory - $availableMemory
    $memoryUsage = ($usedMemory / $totalMemory) * 100

    return [PSCustomObject]@{
        TotalMemory = "{0:N2} GB" -f ($totalMemory / 1GB)
        AvailableMemory = "{0:N2} GB" -f ($availableMemory / 1GB)
        UsedMemory = "{0:N2} GB" -f ($usedMemory / 1GB)
        MemoryUsage = "{0:N2}%" -f $memoryUsage
    }
}

# 函数：获取系统兼容性信息
function Get-CompatibilityInfo {
    $osInfo = Get-WmiObject Win32_OperatingSystem
    $processorInfo = Get-WmiObject Win32_Processor
    $videoController = Get-WmiObject Win32_VideoController

    $compatibilityInfo = [PSCustomObject]@{
        OS64Bit = $osInfo.OSArchitecture -eq "64-bit"
        ProcessorArchitecture = $processorInfo.AddressWidth
        ProcessorVirtualizationEnabled = $processorInfo.VirtualizationFirmwareEnabled
        UEFI = (Get-ItemProperty "HKLM:\System\CurrentControlSet\Control\SecureBoot\State" -ErrorAction SilentlyContinue).UEFISecureBootEnabled
        TPM = $null -ne (Get-WmiObject -Namespace root\cimv2\security\microsofttpm -Class win32_tpm -ErrorAction SilentlyContinue)
        DX12Support = $videoController.AdapterCompatibility -match "NVIDIA|AMD|Intel"
    }

    return $compatibilityInfo
}

# 主函数：收集并输出所有信息
function Get-DetailedSystemInfo {
    Write-Host "======== Screen Information ========" -ForegroundColor Cyan
    Get-ScreenInfo | Format-Table -AutoSize

    Write-Host "======== Display Adapter Information ========" -ForegroundColor Cyan
    Get-DisplayAdapterInfo | Format-Table -AutoSize

    Write-Host "======== Monitor Information ========" -ForegroundColor Cyan
    Get-MonitorInfo | Format-Table -AutoSize

    Write-Host "======== DPI Settings ========" -ForegroundColor Cyan
    Write-Host "System DPI: $(Get-DpiSetting)"

    Write-Host "======== System Information ========" -ForegroundColor Cyan
    Get-SystemInfo | Format-List

    Write-Host "======== Processor Information ========" -ForegroundColor Cyan
    Get-ProcessorInfo | Format-List

    Write-Host "======== Memory Information ========" -ForegroundColor Cyan
    Get-MemoryInfo | Format-Table -AutoSize

    Write-Host "======== Detailed Memory Usage ========" -ForegroundColor Cyan
    Get-DetailedMemoryInfo | Format-List

    Write-Host "======== Disk Information ========" -ForegroundColor Cyan
    Get-DiskInfo | Format-Table -AutoSize

    Write-Host "======== Network Adapter Information ========" -ForegroundColor Cyan
    Get-NetworkAdapterInfo | Format-Table -AutoSize

    Write-Host "======== BIOS Information ========" -ForegroundColor Cyan
    Get-BiosInfo | Format-List

    Write-Host "======== Operating System Information ========" -ForegroundColor Cyan
    Get-OSInfo | Format-List

    Write-Host "======== DirectX Version ========" -ForegroundColor Cyan
    Write-Host "DirectX Version: $(Get-DirectXVersion)"

    
    Write-Host "======== Recent Error Logs ========" -ForegroundColor Cyan
    Get-EventLog -LogName System -EntryType Error -Newest 10 | 
        Select-Object TimeGenerated, Source, Message | Format-Table -AutoSize

    

    Write-Host "======== System Compatibility Information ========" -ForegroundColor Cyan
    Get-CompatibilityInfo | Format-List

    Write-Host "======== Additional GPU Information ========" -ForegroundColor Cyan
    Get-WmiObject Win32_VideoController | ForEach-Object {
        Write-Host "GPU Name: $($_.Name)"
        Write-Host "Video Processor: $($_.VideoProcessor)"
        Write-Host "Video Memory: $([math]::Round($_.AdapterRAM / 1GB, 2)) GB"
        Write-Host "Current Resolution: $($_.CurrentHorizontalResolution) x $($_.CurrentVerticalResolution)"
        Write-Host "Max Refresh Rate: $($_.MaxRefreshRate) Hz"
        Write-Host "Driver Version: $($_.DriverVersion)"
        Write-Host "DirectX Support: $($_.AdapterDACType)"
        Write-Host ""
    }

    Write-Host "======== Installed Software ========" -ForegroundColor Cyan
    Get-WmiObject Win32_Product | Select-Object Name, Version | Format-Table -AutoSize

    Write-Host "======== Windows Updates ========" -ForegroundColor Cyan
    Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10 | Format-Table -AutoSize

    Write-Host "======== Power Plan Information ========" -ForegroundColor Cyan
    powercfg /list

    Write-Host "======== System Devices ========" -ForegroundColor Cyan
    Get-WmiObject Win32_PnPEntity | Where-Object { $_.ConfigManagerErrorCode -eq 0 } | 
        Select-Object Name, DeviceID | Format-Table -AutoSize

    Write-Host "======== Running Processes ========" -ForegroundColor Cyan
    Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 | 
        Format-Table Name, ID, CPU, WorkingSet -AutoSize

    Write-Host "======== Network Information ========" -ForegroundColor Cyan
    ipconfig /all

    Write-Host "======== Firewall Status ========" -ForegroundColor Cyan
    netsh advfirewall show allprofiles state

    Write-Host "======== System Drivers ========" -ForegroundColor Cyan
    Get-WmiObject Win32_SystemDriver | Where-Object { $_.State -eq "Running" } | 
        Select-Object DisplayName, Name, State | Format-Table -AutoSize
}

# 执行主函数并将输出保存到文件
$outputFile = "SystemInfo_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Get-DetailedSystemInfo | Tee-Object -FilePath $outputFile

Write-Host "System information has been saved to $outputFile" -ForegroundColor Green

# 等待用户输入以防止脚本立即退出
Read-Host -Prompt "Press Enter to exit"
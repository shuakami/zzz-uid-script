<p align="center">
  <img src="./banner.png" alt="ZZZ (绝区零) UID 脚本横幅" width="100%"/>
</p>

# ZZZ (绝区零) 自动登录脚本

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/Language-English-red.svg" alt="Language">
  </a>
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/许可证-自定义 MIT-green.svg" alt="许可证">
  <img src="https://img.shields.io/badge/平台-Windows-lightgrey.svg" alt="平台">
  <img src="https://img.shields.io/badge/Python-3.11+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-API-orange.svg" alt="OpenAI API">
  <img src="https://img.shields.io/badge/基于-米哈游启动器-purple.svg" alt="米哈游启动器">
</p>

<p align="center">
  精准可靠地自动化您的ZZZ（绝区零）UID预约流程。
</p>

<p align="center">
  <a href="#核心功能">核心功能</a> •
  <a href="#系统要求">系统要求</a> •
  <a href="#安装步骤">安装步骤</a> •
  <a href="#配置说明">配置说明</a> •
  <a href="#使用方法">使用方法</a> •
  <a href="#日志系统">日志系统</a> •
  <a href="#故障排除">故障排除</a> •
  <a href="#常见问题">常见问题</a> •
  <a href="#参与贡献">参与贡献</a> •
  <a href="#许可说明">许可说明</a>
</p>


## 核心功能

- 🚀 自动化Python安装和环境配置
- 🔐 与OpenAI API安全集成，增强功能性
- 🖼️ 先进的图像识别技术，实现UI智能导航
- ⏰ 精确定时执行
- 🔄 自动更新和维护
- 📊 全面的日志系统，便于调试和分析

## 系统要求

使用前请确保满足以下条件：

- Windows 10 或更高版本
- PowerShell 5.1 或更高版本
- 稳定的网络连接
- 100GB以上可用磁盘空间
- 确保你的[米哈游启动器](https://launcher.mihoyo.com/)安装在`C:\Program Files\miHoYo Launcher`

## 安装步骤

1. **克隆仓库**
   ```powershell
   git clone https://github.com/shuakami/zzz-uid-script.git
   cd zzz-uid-script
   ```

2. **安装Python**
   （以管理员身份运行）：
   ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    Y
   .\JS\InstallPython311.ps1
   ```

3. **环境设置（可选，用于定时执行）**
   设置7月4日早上7点自动执行：
   ```powershell
   .\JS\SetLive.ps1
   ```
   
4. [配置](#配置说明)

## 配置说明

1. 编辑 `config.py`：
   ```python
   # OpenAI API 配置
   OPENAI_API_KEY = "你的OpenAI API密钥"
   OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

   # 日志配置
   LOG_FILE = "auto_uid_grabber.log"
   LOG_LEVEL = "INFO"
   ```

2. **重要**：运行前，在 `/password/default.txt` 中输入您的账号凭证：
   ```
   账号,密码
   ```

## 使用方法

### 自动执行
如果运行了 `SetLive.ps1`，脚本将在7月4日早上7点自动执行。

### 手动执行
手动运行步骤：
1. 以管理员身份打开PowerShell
2. 导航至脚本目录
3. 执行：
   ```powershell
   python start_ocr.py
   ```

## 日志系统

脚本生成多个日志文件用于监控和故障排除：

- `game-main.log`：核心UID预约组件日志
- `game_login.log`：`start_ocr.py` 的运行日志
- `login.log`：身份验证过程日志
- `install.log`：安装过程日志

## 故障排除

遇到问题时：

1. 检查脚本目录中的相关日志文件。
2. 确保满足所有系统要求。
3. 验证网络连接是否正常。
4. 确认 `config.py` 中的OpenAI API密钥设置正确。

常见问题：
- **脚本无法启动**：以管理员身份运行PowerShell。
- **图像识别问题**：确保 `dist` 文件夹中的截图与您的启动器界面匹配。
- **API错误**：检查OpenAI API密钥和网络连接。

## 常见问题

问：这个脚本可以在macOS或Linux上使用吗？
答：目前仅支持Windows系统，因为脚本基于米哈游启动器集成。

问：在脚本中使用我的OpenAI API密钥安全吗？
答：是的，但切勿分享您的 `config.py` 文件或API密钥。脚本仅在您的本地机器上使用该密钥。

问：这个脚本能保证我获得UID吗？
答：虽然脚本自动化了预约过程，但由于服务器限制和高需求，不能保证100%成功。

问：我可以修改执行时间吗？
答：可以，通过编辑 `SetLive.ps1` 来更改。请确保遵守官方关于UID预约过程的指导原则。

## 参与贡献

我们欢迎对ZZZ UID自动预约脚本的贡献！参与方式：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m '添加了一些很棒的功能'`)
4. 将您的更改推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

请遵守项目的编码标准，并包含适当的测试。

## 许可说明

本项目采用自定义MIT许可证 - 详情请见 [LICENSE.md](LICENSE.md) 文件。

**重要提示**：严禁商业使用。本软件仅供个人使用。

## 声明

严禁 https://gitcode.com/ (GitCode) 或任何其他未经授权的实体抓取或复制本仓库。

![GitCode Logo](!gitdog-logo.png)

## 免责声明

* 图像免责声明：项目使用的横幅图像包含来自《绝区零》的素材，其版权归米哈游/HoYoverse所有。该图像仅用于说明目的，基于教育和非商业用途的合理使用原则。我们不对原始艺术作品主张任何所有权，如版权所有者要求，我们将立即删除。


- 本脚本与米哈游没有任何关联，也未得到米哈游的认可或赞助。 使用本脚本需自担风险，并确保遵守所有相关服务条款。


- 本脚本仅供学习和研究用途，使用者须自行承担所有风险。脚本开发者及所有相关方对因使用本脚本而可能产生的任何直接或间接损失概不负责。


- 本脚本与米哈游或任何其他游戏开发商没有任何关联，也未获得其认可或授权。使用本脚本可能违反游戏的服务条款，可能导致账号被封禁等处罚。使用者需自行承担所有相关风险。


- 脚本不保证能够成功预约UID或提供任何特定结果。脚本的功能可能因游戏更新、服务器变动等因素而失效，开发者不承诺提供及时的更新或维护。


- 严禁将本脚本用于任何商业目的。不得销售、出租、转让本脚本或利用本脚本牟利。


- 免责范围在法律允许的最大范围内，开发者不对任何损失承担责任，包括但不限于：数据丢失、账号被封、财产损失、声誉损害等。


- **如果您不同意本协议的任何部分，请立即停止使用本脚本并删除所有相关文件。**

## 免责声明和责任限制

本ZZZ（绝区零）UID自动预约脚本（以下简称"脚本"）按"原样"和"可用性"提供，不作任何明示或暗示的陈述或保证。开发者Shuakami<SdjzWiki>及所有相关方：

1. 不对脚本或其功能作任何陈述或保证。
2. 不保证脚本的准确性、及时性、性能、完整性或适用性。
3. 不对脚本内容中的任何错误或遗漏负责。
4. 不对因使用或无法使用脚本而导致的任何直接、间接、后果性或附带损害承担责任。
5. 不对米哈游或任何第三方因使用本脚本而采取的行动负责。
6. 不保证OpenAI API或脚本使用的任何其他第三方服务的可用性或连续性。

使用本脚本即表示您承认并同意：

1. 您自行承担使用脚本的风险。
2. 您对因使用脚本而可能产生的任何后果承担全部责任。
3. 您将遵守使用脚本时的所有适用法律和法规。
4. 您不会将脚本用于任何非法、不道德或未经授权的目的。
5. 未经明确许可，您不会尝试对脚本进行逆向工程、修改或分发。
6. 您确保本脚本不得用于任何违反游戏服务条款的行为，包括但不限于作弊和自动操作。
7. 您需要在使用前需确认已阅读并理解游戏服务条款，并同意在合法框架内使用脚本。
8. 使用脚本即代表您已经充分理解并同意所有相关的法律法规和游戏服务条款。

开发者保留随时修改、暂停或终止脚本的权利，恕不另行通知。本免责声明可能会不时更新，恕不另行通知。

---

<p align="center">
  Developed with ❤️ by Shuakami<SdjzWiki>
</p>

<p align="center">
  <img src="./banner.png" alt="ZZZ (Zenless) UID Script Banner" width="100%"/>
</p>

# ZZZ (Zenless) Login Auto-Reservation Script

<p align="center">
  <a href="README_zh.md">
    <img src="https://img.shields.io/badge/点我切换语言-red.svg" alt="中文">
  </a>
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-Custom_MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.11+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-API-orange.svg" alt="OpenAI API">
  <img src="https://img.shields.io/badge/miHoYo-Launcher-purple.svg" alt="miHoYo Launcher">
</p>

<p align="center">
  Automate your ZZZ (Zenless Zone Zero) UID reservation process with precision and reliability.
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#installation">Installation</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#logging">Logging</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#faq">FAQ</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Key Features

- 🚀 Automated Python installation and environment setup
- 🔐 Secure integration with OpenAI API for enhanced functionality
- 🖼️ Advanced image recognition for UI navigation
- ⏰ Scheduled execution for precise timing
- 🔄 Automatic updates and maintenance
- 📊 Comprehensive logging system for debugging and analysis

## Prerequisites

Before proceeding, ensure you have:

- Windows 10 or later
- PowerShell 5.1 or later
- Stable internet connection
- 100GB+ free disk space
- [miHoYo Launcher](https://launcher.mihoyo.com/) installed at `C:\Program Files\miHoYo Launcher`

## Installation

1. **Clone the Repository**
   ```powershell
   git clone https://github.com/shuakami/zzz-uid-script.git
   cd zzz-uid-script
   ```

2. **Install Python**
   Run as Administrator:
   ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    Y
   .\JS\InstallPython311.ps1
   ```

3. **Set Up Environment (Optional for Scheduled Execution)**
   For automatic execution on July 4th at 7 AM:
   ```powershell
   .\JS\SetLive.ps1
   ```
   
4. [Configuration](#Configuration)

## Configuration

1. Edit `config.py`:
   ```python
   # OpenAI API Configuration
   OPENAI_API_KEY = "your_openai_api_key"
   OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

   # Logging Configuration
   LOG_FILE = "auto_uid_grabber.log"
   LOG_LEVEL = "INFO"
   ```

2. **Important**: Before running, enter your account credentials in `/password/default.txt`:
   ```
   account,password
   ```

## Usage

### Automatic Execution
If `SetLive.ps1` was run, the script will execute automatically on July 4th at 7 AM.

### Manual Execution
To run manually:
1. Open PowerShell as Administrator
2. Navigate to the script directory
3. Execute:
   ```powershell
   python start_ocr.py
   ```

## Logging

The script generates several log files for monitoring and troubleshooting:

- `game-main.log`: Core UID reservation component logs
- `game_login.log`: Logs from `start_ocr.py`
- `login.log`: Authentication process logs
- `install.log`: Installation process logs

## Troubleshooting

If you encounter issues:

1. Check the relevant log files in the script directory.
2. Ensure all prerequisites are met.
3. Verify your internet connection.
4. Confirm your OpenAI API key is correctly set in `config.py`.

Common issues:
- **Script fails to start**: Run PowerShell as Administrator.
- **Image recognition issues**: Verify screenshots in the `dist` folder match your launcher's appearance.
- **API errors**: Check your OpenAI API key and internet connection.

## FAQ

Q: Is this script compatible with macOS or Linux?
A: Currently, it's designed for Windows only due to miHoYo Launcher integration.

Q: Is using my OpenAI API key in the script safe?
A: Yes, but never share your `config.py` or API key. The script uses the key locally on your machine.

Q: Does this script guarantee a UID?
A: While it automates the process, success isn't guaranteed due to server limitations and high demand.

Q: Can I modify the execution schedule?
A: Yes, by editing `SetLive.ps1`. Ensure compliance with official guidelines regarding the UID reservation process.

## Contributing

We welcome contributions to the ZZZ UID Auto-Reservation Script! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please adhere to the project's coding standards and include appropriate tests.

## License

This project is licensed under a custom MIT License - see the [LICENSE.md](LICENSE.md) file for details. 

**Important**: Commercial use is strictly prohibited. This software is for personal use only.

## Legal Notice

Scraping or copying this repository by https://gitcode.com/ (GitCode) or any other unauthorized entities is strictly prohibited.

![GitCode Logo](!gitdog-logo.png)

## Disclaimer

* Image Disclaimer: The banner image used in this project contains material from Zenless Zone Zero, which is the property of miHoYo/HoYoverse. This image is used for illustrative purposes only, under fair use for educational and non-commercial purposes. We claim no ownership of the original artwork and will remove it immediately upon request from the copyright holder.

- This script is not affiliated with miHoYo, nor is it endorsed or sponsored by miHoYo. Use this script at your own risk and ensure compliance with all applicable service terms.


- This script is intended for educational and research purposes only. Users must assume all risks associated with its use. The script developers and all related parties are not responsible for any direct or indirect losses that may result from the use of this script.


- This script is not affiliated with miHoYo or any other game developers, nor has it been approved or authorized by them. Using this script may violate the game's terms of service and could lead to penalties such as account suspension. Users must bear all related risks.


- The script does not guarantee successful UID booking or any specific outcomes. Its functionality may be compromised by updates to the game, changes in servers, and other factors. The developers do not commit to providing timely updates or maintenance.


- The use of this script for commercial purposes is strictly prohibited. It may not be sold, rented, transferred, or used for profit in any way.


- To the maximum extent permitted by law, the developers disclaim any liability for any losses, including but not limited to: data loss, account suspension, property damage, or reputational harm.


- **If you do not agree with any part of this agreement, please stop using this script immediately and delete all related files.**

## Disclaimer and Limitation of Liability

This ZZZ (Zenless) UID Auto-Reservation Script (the "Script") is provided "as is" and "as available", without any representations or warranties of any kind, either express or implied. The developer, Shuakami<SdjzWiki>, and all associated parties:

1. Make no representations or warranties in relation to the Script or its functionality.
2. Do not guarantee the accuracy, timeliness, performance, completeness, or suitability of the Script for any purpose.
3. Are not responsible for any errors or omissions in the content of the Script.
4. Are not liable for any direct, indirect, consequential, or incidental damages arising from the use or inability to use the Script.
5. Are not responsible for any actions taken by miHoYo or any other third party in response to the use of this Script.
6. Do not guarantee the availability or continuity of the OpenAI API or any other third-party services used by the Script.

By using this Script, you acknowledge and agree that:

1. You use the Script at your own risk and discretion.
2. You are solely responsible for any consequences that may arise from your use of the Script.
3. You will comply with all applicable laws and regulations in your use of the Script.
4. You will not use the Script for any illegal, unethical, or unauthorized purposes.
5. You will not attempt to reverse engineer, modify, or distribute the Script without explicit permission.
6. You ensure that this script will not be used for any activities that violate the game's terms of service, including but not limited to cheating and automation.
7. You must confirm that you have read and understood the game’s terms of service before using the script and agree to use the script within a legal framework.
8. Using this script signifies that you have fully understood and agreed to all relevant legal regulations and the game’s terms of service.


The developers reserve the right to modify, suspend, or discontinue the Script at any time without notice. This disclaimer may be updated from time to time without prior notice.

---

<p align="center">
  Developed with ❤️ by Shuakami<SdjzWiki>
</p>

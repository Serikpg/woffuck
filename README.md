# woffuck

## Auto-Signer for woffu.com platform

This script automates the process of signing in (clocking in/out) to the Woffu HR platform. It utilizes **Selenium** to handle the browser-based login interaction and **Requests** to execute the signing action via the internal API.

## 📋 Prerequisites

Before running the script, ensure you have the following installed:

1.  Python 3.10.12 or higher
2.  Google Chrome Browser (The script runs an automated instance of Chrome). It can be used with chromium-based browsers too.

## ⚙️ Installation

1.  **Clone or Download** the repository.

    ```bash
    git clone git@github.com:Serikpg/woffuck.git
    ```

2.  **Install the required Python packages**:

    ```bash
    pip install selenium requests
    ```

## 🔐 Configuration

For security reasons, this script does not hardcode credentials. You must set them as **Environment Variables** on your system.

### Option A: Linux / macOS (Terminal)
Run these commands before running the script:
```bash
export WOFFU_EMAIL="your_email@bsc.es"
export WOFFU_PASSWORD="your_secure_password"
export WOFFU_URL="https://example.woffu.com"
```

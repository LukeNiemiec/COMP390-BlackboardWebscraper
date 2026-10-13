---

# Blackboard Webscraper

A Python-based Selenium automation tool designed to persist browser sessions and cookies using a dedicated Firefox profile. The script initially attempts to run in **headless** mode; if an active session is not found, it launches a standard browser window allowing you to log in manually, saving your authenticated state for subsequent headless runs.

---

## Features

- **Persistent Sessions:** Uses a dedicated Firefox user profile to preserve cookies, sessions, and credentials across runs.
- **Headless-First Operation:** Runs silently in the background unless authentication is required.
- **Interactive Login Fallback:** Automatically switches to an interactive GUI mode if login credentials have expired or are missing.

---

## Getting Started

Follow these steps to set up the prerequisites and configure the script on your system.

### 1. Install Selenium
Install the Selenium package via `pip`:

```bash
pip install selenium
```

### 2. Download Firefox and GeckoDriver
This script requires both the Mozilla Firefox browser and the GeckoDriver binary:

1. **Firefox:** Download and install the latest version of [Mozilla Firefox](https://www.mozilla.org/firefox/) if you haven't already.
2. **GeckoDriver:** Download the appropriate [GeckoDriver release](https://github.com/mozilla/geckodriver/releases) for your operating system. Extract the binary and place it in a directory listed in your system `PATH` (e.g., `/usr/local/bin` on Linux/macOS, or alongside your Python scripts on Windows).

> ⚠️ **Important:** Keep track of both your **Firefox executable path** and your **GeckoDriver binary location**. You may need to reference these paths directly using Selenium's `Service` object or `binary_location` option if they are not installed in default system directories.

### 3. Create a Dedicated Firefox Profile
To prevent conflicts with your personal browsing data and to store your login cookies persistently, create a separate Firefox profile:

1. Close all active instances of Firefox.
2. Open your terminal or command prompt and run:
   ```bash
   firefox --ProfileManager
   ```
   *(On macOS, run `/Applications/Firefox.app/Contents/MacOS/firefox --ProfileManager`)*
3. In the Profile Manager window, click **Create Profile...**.
4. Name the profile (e.g., `Blackboard`) and complete the wizard.
5. Note the directory path where this profile is created:
   - **Linux:** `~/.mozilla/firefox/<random_hash>.Blackboard/`
   - **macOS:** `~/Library/Application Support/Firefox/Profiles/<random_hash>.Blackboard/`
   - **Windows:** `%APPDATA%\Mozilla\Firefox\Profiles\<random_hash>.Blackboard\`

### 4. Configure the Script
Open the script and update the `PROFILE_DIR` constant with the absolute path to the profile folder you just created:

```python
# Update this with the path to your created profile directory
PROFILE_DIR = "/home/box/.mozilla/firefox/8wbgzkd7.Blackboard"
```

If necessary, you can also change the target URL in the `__main__` block:

```python
browser = Browser("https://bridgew.blackboard.com/ultra/course")
```

---

## Usage

Run the script directly using Python:

```bash
python main.py
```

### How Authentication Works:
1. **First Run (Unauthenticated):**
   - The script attempts to open the target URL in headless mode.
   - It detects that you are redirected away from the target page (i.e., sent to an SSO/login page).
   - It re-opens in standard GUI mode and prompts you in the terminal:
     ```text
     [+] Press enter once you have finished logging in
     ```
   - Log in manually via the browser window, complete any 2FA/MFA challenges, and press **Enter** in the terminal.
   - Your session is now saved inside the profile directory.

2. **Subsequent Runs (Authenticated):**
   - The script loads the profile with your saved cookies and session data in **headless mode**, bypassing the login prompt directly.

---

## Troubleshooting

- **GeckoDriver not found:** Ensure the directory containing `geckodriver` is added to your system `PATH`.
- **Profile lock error:** Make sure no other Firefox windows using the designated profile are running when you execute the script.

---

### Whats Next

- **Configure Selenium Downloads:** Make sure that selenium can download files from blackboard.
- **HTML Element Extraction:** Find the right HTML elements to find on what page and get the desired content.

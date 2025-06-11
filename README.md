# Outlook File Downloader Bot

Automates the daily routine of logging into Outlook Web, locating a specific email, following an embedded link, and downloading a spreadsheet file—all hands‑free.

---

## ✨ Key Features

| Step | Action                          | Tech                                                       | Notes                                                    |
| ---- | ------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| 1    | Launch Chrome (undetected)      | SeleniumBase `Driver(uc=True)`                             | Maximised window to avoid hidden elements.               |
| 2    | Navigate to Outlook Web         | `https://outlook.live.com/mail/0/`                         | Reconnect logic for robustness.                          |
| 3    | Sign‑in                         | Standard login ➜ Password ➜ TOTP                           | Credentials & secret key loaded from **.env**.           |
| 4    | Handle 2‑factor (TOTP)          | `pyotp`                                                    | Fallback locators for both single‑box and 6‑box layouts. |
| 5    | Search mailbox                  | Query from **SEARCH\_CONTENT** env var                     | Clicks top result in message list.                       |
| 6    | Open reading pane & follow link | Reliable XPath (`//div[@aria-label="Message body"]//a[1]`) | Works even if email template changes.                    |
| 7    | Switch to new tab               | Window‑handle strategy                                     | Always operates on newest tab.                           |
| 8    | Download target file            | CSS selector `.text-right.file-link > a`                   | Scrolls to bottom first.                                 |

---

## 📂 Repository Structure

```
├── main.py              # Automation script
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

## 🖥️ Prerequisites

* **Python 3.10 or newer**
* **Google Chrome 115+** (matching versions of Chrome & ChromeDriver)
* Windows, macOS, or Linux

---

## 🔧 Installation

```bash
# 1 – Clone the repo
$ git clone https://github.com/your‑org/outlook‑file‑downloader.git
$ cd outlook‑file‑downloader

# 2 – Create & activate a virtual environment (recommended)
$ python -m venv .venv
$ source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3 – Install dependencies
$ pip install -r requirements.txt
```

**requirements.txt** (for reference):

```
seleniumbase==4.*
webdriver-manager==4.*
python-dotenv==1.*
pyotp==2.*
```

---

## 🔑 Environment Variables

Create a **.env** file in the project root:

```ini
EMAIL=your_outlook_email@example.com
PASSWORD=your_outlook_password
SECRET_KEY=BASE32TOTPSECRET123   # Used by pyotp to generate 6‑digit codes
SECURE_PASS = 'Secure Password'
```

> **Security Tip** – Do **not** commit `.env` to version control. Add it to `.gitignore`.

---

## 🚀 Usage

```bash
# Ensure Chrome is closed or no sensitive sessions are open.
$ python main.py
```

The console will show step‑by‑step logs:

```
Opening Website…
Moving to sign‑in steps …
Email Entered.
Password Entered.
OTP Entered.
Logged In to Outlook Successfully.
Searched for content.
Selected first search result.
Clicked on the link.
Scrolling Done.
Waiting for file to download…
Process Done.
```

Downloaded files land in Chrome’s default download directory unless you customise it via Chrome options.

---

## 🛠️ Customisation & Tips

| Area                | How to tweak                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Download folder** | Edit `chrome_options` in `main.py` and set `prefs["download.default_directory"]`.           |
| **Timeouts**        | Change `WebDriverWait(driver, seconds)` values for slow networks.                           |
| **Search logic**    | Adjust XPath inside `first_search` if you need the *nth* email or by date.                  |
| **OTP Source**      | Swap `pyotp` with push or SMS if your account uses different 2FA.                           |
| **Headless mode**   | Uncomment `chrome_options.add_argument('--headless=new')` (make sure to set a window size). |

---

## 🐞 Troubleshooting

| Problem                             | Likely Cause                           | Fix                                                   |
| ----------------------------------- | -------------------------------------- | ----------------------------------------------------- |
| **ElementNotInteractableException** | Outlook UI changed                     | Update XPath/CSS selectors.                           |
| **TimeoutException on login**       | Incorrect credentials or picker screen | Check `EMAIL`, `PASSWORD`, TOTP, and consent prompts. |
| **Download link not found**         | Page structure changed                 | Inspect HTML and update `first_link` selector.        |

Enable verbose SeleniumBase logs with `pytest -s` or set `--headless --uc-debug` flags for deeper diagnostics.

---

## 📜 License

This project is released under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ✍️ Author

*Rushikesh Borkar* – Contact: `borkarrushi028@gmail.com` !

# 🤖 TelegramSelfBot

A **Telegram userbot (selfbot)** built in Python with [Pyrogram](https://docs.pyrogram.org/) that runs directly on your personal Telegram account (not a BotFather bot). It adds a live clock to your display name, reveals outgoing messages with a typewriter-style edit animation, runs playful text animations, and can manage **multiple Telegram accounts at once** from a single instance.

> ⚠️ **Disclaimer:** Automating a personal account with a userbot is against [Telegram's Terms of Service](https://core.telegram.org/api/terms) and can get your account **limited or banned**. This project is provided for educational purposes only — use it at your own risk.

---

## ✨ Features

- **Live clock in your name** — automatically appends the current time (`HH:MM`) to your first name, updated every minute, with a fully customizable digit "font"
- **Typewriter message reveal** — gradually edits your outgoing messages character-by-character/chunk-by-chunk instead of sending them instantly (speed scales with message length)
- **Fun text animations** — a set of built-in emoji/ASCII animations: `gun`, `love`, `emoji`, `heart`, `iloveyou`, `moon`, `cat`, `mew`
- **Per-account settings** — every account has its own on/off state, clock toggle, edit toggle, edit speed, and font, stored in SQLite
- **Multi-account manager** — run several Telegram accounts simultaneously from one process, with newly added accounts picked up automatically (checked every 30 minutes) without restarting
- **Self-cleaning replies** — settings confirmations and animation results auto-delete themselves after a short delay
- **`.me`-only commands** — every command only responds to messages sent by the account owner (`filters.me`), so nobody else can trigger it

---

## 🗂️ Project Structure

```
TelegramSelfBot/
├── main.py                    # Entry point: loads all accounts, starts the sync loop and the clock scheduler
├── addaccount.py               # Standalone CLI script to log in a new account (phone + code + optional 2FA) and save it to the DB
├── config.py                    # Env vars (API_ID/API_HASH), command keywords, reply texts, default font
├── requirements.txt
│
├── database/
│   └── db.py                    # SQLite wrapper (`Database`) + per-user settings object (`User`)
│
├── manager/
│   ├── account_manager.py       # `AccountManager`: creates/starts Pyrogram clients for every stored account
│   └── time_manager.py           # Background scheduler that updates each enabled account's name with the current time every minute
│
├── handlers/
│   ├── register.py               # Registers all Pyrogram MessageHandlers (settings, animations, outgoing messages)
│   ├── commands.py                # Handles /help, /vaziat, /on, /off, /timeon, /timeoff, /font, /editon, /editoff, /settime
│   ├── animations.py              # Handles the fun animation commands
│   └── outgoing_messages.py       # Implements the typewriter-style auto-edit for outgoing text messages
│
├── data/
│   └── animations.py              # Raw animation frame data (text + delay per frame) for each animation command
│
├── utils/
│   └── telegram.py                # Small helpers, e.g. `auto_delete()` to remove a message after N seconds
│
├── database.db                   # SQLite database (created automatically on first run)
└── *.session                      # Pyrogram session files (created automatically)
```

---

## ⚙️ Requirements

- Python 3.9+
- A Telegram **API_ID** and **API_HASH** from [my.telegram.org](https://my.telegram.org)
- The phone number(s) of the account(s) you want to run the userbot on

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PyWizs/TelegramSelfBot.git
cd TelegramSelfBot
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

> `requirements.txt` lists `pyrogram` and `dotenv`. If you run into import errors with `dotenv`, install the correct package explicitly: `pip install python-dotenv`. Installing `TgCrypto` (`pip install TgCrypto`) is also recommended for better Pyrogram performance, though not required.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
API_ID=123456
API_HASH=your_api_hash_here
```

### 4. Add a Telegram account

Run the login script and follow the prompts (phone number, login code, and 2FA password if enabled):

```bash
python addaccount.py
```

This logs in with Pyrogram, exports a session string, and saves the account into `database.db`. Repeat this step for every additional account you want the bot to manage.

### 5. Run the bot

```bash
python main.py
```

All accounts stored in the database are loaded and started automatically. New accounts added later (via `addaccount.py`) are picked up within 30 minutes without needing a restart.

---

## 💬 Commands

Send these as messages from your own account (e.g. in "Saved Messages") — only messages from the account owner are recognized.

| Command | Description |
|---|---|
| `/help` | Show the full command list |
| `/vaziat` | Show the bot's current status (enabled, clock, auto-edit, edit speed, font) |
| `/sargarmi` | Show the list of fun animation commands |
| `/on` | Enable the bot for this account |
| `/off` | Disable the bot for this account |
| `/timeon` | Enable the live clock in your display name |
| `/timeoff` | Disable the live clock and restore your original name |
| `/font <11 characters>` | Set the digit font used for the clock — must be exactly 11 characters (digits `0-9` + `:`), e.g. `/font 0123456789:` |
| `/editon` | Enable the typewriter auto-edit effect on your outgoing messages |
| `/editoff` | Disable the typewriter auto-edit effect |
| `/settime <seconds>` | Set the delay (in seconds) between each edit step |
| `/gun`, `/love`, `/emoji`, `/heart`, `/iloveyou`, `/moon`, `/cat`, `/mew` | Play a fun text animation by editing the message repeatedly |

---

## 🧠 How it works

- **`AccountManager`** loads every account row from SQLite, spins up a Pyrogram `Client` per account using its stored `session_string`, attaches a `User` settings object to `client.user`, and registers all handlers.
- **`time_manager.scheduler`** runs in the background and, once per minute, updates the display name of every account that has both `enabled` and `show_time` turned on, mapping each digit/colon of `HH:MM` through the account's custom font.
- **`outgoing_messages.outgoing_handler`** intercepts your own outgoing text messages when `edit_enabled` is on, and reveals them gradually via repeated `message.edit()` calls — the reveal chunk size depends on message length (longer messages reveal in bigger steps so it doesn't take forever).
- **`animations.animation_handler`** replays a sequence of pre-defined text frames (from `data/animations.py`) onto the same message via edits, then deletes it after a few seconds.
- Settings and animation replies use `utils.telegram.auto_delete()` to remove themselves after a short delay (20s for settings, 5s for animations), keeping your chat history clean.

---

## 🤝 Contributing

Issues and pull requests are welcome if you'd like to suggest improvements, report bugs, or add new animations/features.

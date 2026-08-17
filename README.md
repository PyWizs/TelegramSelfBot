# 🤖 TelegramSelfBot

A **Telegram userbot (selfbot)** built in Python with [Pyrogram](https://docs.pyrogram.org/) that runs directly on your personal Telegram account (not a BotFather bot). It adds a live clock to your display name, reveals outgoing messages with a typewriter-style edit animation, plays customizable text animations, translates messages on the fly, rescues self-destructing media, and can manage **multiple Telegram accounts at once** from a single instance.

> ⚠️ **Disclaimer:** Automating a personal account with a userbot is against [Telegram's Terms of Service](https://core.telegram.org/api/terms) and can get your account **limited or banned**. This project is provided for educational purposes only — use it at your own risk.

---

## ✨ Features

- **Live clock in your name** — automatically appends the current time (`HH:MM`) to your first name, updated every minute, with a fully customizable digit "font"
- **Typewriter message reveal** — gradually edits your outgoing messages instead of sending them instantly (speed scales with message length)
- **Customizable text animations** — built-in animations (`gun`, `love`, `emoji`, `heart`, `iloveyou`, `moon`, `cat`, `mew`), each with:
  - A configurable repeat count via `--run <n>`, overriding the animation's default
  - An optional custom message wrapped around the animation frame using an `<a>` placeholder, e.g. `/moon Good night <a>`
- **Built-in translator** — translate any message on the spot with `/t`, `/trans`, or `/translate`, powered by [deep-translator](https://github.com/nidhaloff/deep-translator) (Google Translate). The original command is deleted and replaced with the translated text, preserving any reply-to context
- **Multi-language interface** — bot replies (help, status, confirmations, errors) are available in **English and Persian (Farsi)** via `/lang en` / `/lang fa`, backed by simple JSON language files in `lang/` — new languages can be added by dropping in another JSON file
- **Self-destructing media rescue** — automatically downloads and re-sends to "Saved Messages" any incoming disappearing (TTL) photo, video, video note, or voice message received in a private chat, before it can vanish
- **Per-account settings** — every account has its own on/off state, clock toggle, edit toggle, edit speed, font, UI language, and translation target language — stored in SQLite with automatic schema migrations
- **Multi-account manager** — run several Telegram accounts simultaneously from one process; newly added accounts are picked up automatically (checked every 30 minutes) without restarting
- **Self-cleaning replies** — settings confirmations and un-customized animations auto-delete themselves after a short delay
- **`.me`-only commands** — every command only responds to messages sent by the account owner (`filters.me`), so nobody else can trigger it

---

## 🗂️ Project Structure

```
TelegramSelfBot/
├── main.py                    # Entry point: loads all accounts, starts the sync loop and the clock scheduler
├── addaccount.py               # Standalone CLI script to log in a new account (phone + code + optional 2FA) and save it to the DB
├── config.py                    # Env vars (API_ID/API_HASH), command keywords, default font
├── requirements.txt
│
├── lang/
│   ├── en.json                  # English UI strings (help, status, confirmations, errors)
│   └── fa.json                  # Persian UI strings
│
├── database/
│   └── db.py                    # SQLite wrapper (`Database`, with schema migrations) + per-user settings object (`User`)
│
├── manager/
│   ├── account_manager.py       # `AccountManager`: creates/starts a Pyrogram client + LanguageManager for every stored account
│   ├── language_manager.py       # `LanguageManager`: loads `lang/*.json` and resolves translated strings, falling back to the default language
│   └── time_manager.py            # Background scheduler that updates each enabled account's name with the current time every minute
│
├── handlers/
│   ├── register.py               # Registers all Pyrogram MessageHandlers (settings, animations, outgoing messages, media rescue)
│   ├── commands.py                # Handles /help, /vaziat, /on, /off, /timeon, /timeoff, /font, /editon, /editoff, /settime, /lang, /translang, /t
│   ├── animations.py              # Handles the animation commands, including `--run` and `<a>` custom-message support
│   ├── outgoing_messages.py       # Implements the typewriter-style auto-edit for outgoing text messages
│   └── save_media.py               # Downloads and re-sends self-destructing media to Saved Messages
│
├── data/
│   └── animations.py              # Raw animation frame data (text + delay per frame, plus default run count) for each animation command
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

> `requirements.txt` lists `pyrogram`, `dotenv`, and `deep-translator`. If you run into import errors with `dotenv`, install the correct package explicitly: `pip install python-dotenv`. Installing `TgCrypto` (`pip install TgCrypto`) is also recommended for better Pyrogram performance, though not required.

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

All accounts stored in the database are loaded and started automatically. New accounts added later (via `addaccount.py`) are picked up within 30 minutes without needing a restart. The database schema is migrated in place, so upgrading from an older version of this project won't break existing accounts.

---

## 💬 Commands

Send these as messages from your own account (e.g. in "Saved Messages") — only messages from the account owner are recognized.

| Command | Description |
|---|---|
| `/help` | Show the full command list |
| `/vaziat` | Show the bot's current status (enabled, clock, auto-edit, edit speed, font) |
| `/sargarmi` | Show the list of available animations |
| `/on` | Enable the bot for this account |
| `/off` | Disable the bot for this account |
| `/timeon` | Enable the live clock in your display name |
| `/timeoff` | Disable the live clock and restore your original name |
| `/font <11 characters>` | Set the digit font used for the clock — must be exactly 11 characters (digits `0-9` + `:`), e.g. `/font 0123456789:` |
| `/editon` | Enable the typewriter auto-edit effect on your outgoing messages |
| `/editoff` | Disable the typewriter auto-edit effect |
| `/settime <seconds>` | Set the delay (in seconds, decimals allowed) between each edit step |
| `/lang <en\|fa>` | Switch the bot's reply language; run without an argument to see the picker |
| `/translang <code>` | Set the target language for `/t` translations (must be a valid [deep-translator](https://github.com/nidhaloff/deep-translator) language code, e.g. `en`, `fa`, `de`) |
| `/t`, `/trans`, `/translate <text>` | Translate `<text>` into your `translang` and send it (auto-detects the source language; replies to the same message if used as a reply) |
| `/gun`, `/love`, `/emoji`, `/heart`, `/iloveyou`, `/moon`, `/cat`, `/mew` | Play an animation. Add `--run <n>` to repeat it a custom number of times, and/or wrap your own text around it with `<a>` marking where the animation frame goes, e.g. `/cat Look at this <a> --run 2` |

---

## 🧠 How it works

- **`AccountManager`** loads every account row from SQLite, spins up a Pyrogram `Client` per account using its stored `session_string`, attaches a `User` settings object and a `LanguageManager` (initialized to that account's saved language) to the client, and registers all handlers.
- **`LanguageManager`** loads every `*.json` file in `lang/` at startup, keyed by filename (e.g. `en`, `fa`). `translate(language, key)` looks up the string in the requested language, falling back to the default language (and finally the raw key) if missing.
- **`time_manager.scheduler`** runs in the background and, once per minute, updates the display name of every account that has both `enabled` and `show_time` turned on, mapping each digit/colon of `HH:MM` through the account's custom font.
- **`outgoing_messages.outgoing_handler`** intercepts your own outgoing text messages when `edit_enabled` is on, and reveals them gradually via repeated `message.edit()` calls — the reveal chunk size depends on message length.
- **`animations.animation_handler`** replays a sequence of pre-defined text frames (from `data/animations.py`) onto the message via edits. It parses an optional `--run <n>` count and an optional custom message (with `<a>` as the animation-frame placeholder) from the command text, then loops through the animation that many times.
- **`commands.findedKey`** dispatches every settings command, looks up the reply text via `client.lang.translate(...)`, and for `/t`/`/trans`/`/translate` calls out to `GoogleTranslator` (via `deep-translator`), deleting the original command and posting the translated text in its place (preserving reply context).
- **`save_media.save_media`** listens for photos, videos, video notes, and voice messages in private chats; if the incoming media has a `ttl_seconds` (i.e. it's a self-destructing/"view once" message), it's downloaded and immediately re-sent to "Saved Messages" before Telegram deletes it.
- Settings and plain animation replies use `utils.telegram.auto_delete()` to remove themselves after a short delay (20s for settings, 5s for animations without custom text), keeping your chat history clean.

## 🤝 Contributing

Issues and pull requests are welcome if you'd like to suggest improvements, report bugs, add new languages, or add new animations/features.

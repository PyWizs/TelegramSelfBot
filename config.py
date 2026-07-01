from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

TEXTSETTING = {
    "help": """
• **برای دیدن وضعیت ربات بنویسید:** /vaziat
• **برای دیدن سرگرمی ربات بنویسید:** /sargarmi

• **برای خاموش کردن ربات**: /off
• **برای روشن کردن ربات**: /on

• **برای خاموش کردن تغییر نام**: /timeoff
• **برای روشن کردن ساعت در تغییر نام**: /timeon
• **برای تغییر فونت ساعت تایم**: /font 0123456789:

• **برای خاموش کردن ادیت مسیج**: /editoff
• **برای روشن کردن ادیت مسیج**: /editon
• **برای تنظیم سرعت ادیت مسیج**: /settime <زمان به ثانیه>
""",
    "sargarmi": """
• لیست تمامی سرگرمی ها:

/gun
/love
/emoji
/heart
/iloveyou
/moon
/cat
/mew
""",
    "vaziat": """
🎭 وضغیت ربات:

• ربات روشنه؟ : {}
• تغییر نام روشنه؟ : {}
• ادیت مسیج روشنه؟ : {}
• سرعت ادیت مسیح : {}
• فونت ساعت : {}
""",
    "offBot": "• ربات خاموش شد. 😔", #
    "onBot": "• ربات روشن شد. 😝", #
    "timeOff": "• تغییر نام خاموش شد. ⌚", #
    "timeOn": "• تغییر نام روشن شد. ⏰", #
    "editMsgOff": "• ادیت مسیج خاموش شد. 🫣", #
    "editMsgOn": "• ادیت مسیح روشن شد. 🤪", #
    "editFont": "• فونت ساعت با موفقیت تغییر کرد. ⏱️",
    "editFontERROR": "• تغییر فونت با موشکل مواجه شد 🌋\n* ارور: نامشخص",
    "setTime": "• سرعت ادیت مسیج تغییر کرد. 🏃", #
    "setTimeERROR": "• تغییر سرعت ادیت مسیج با مشکل مواجه شد 🌋\n* ارور: نامشخص" #
}

KEYWORD = {
    "help": ["help"],
    "sargarmi": ["sargarmi"],
    "vaziat": ["vaziat"],
    "offBot": ["off"],
    "onBot": ["on"],
    "timeOff": ["timeoff"],
    "timeOn": ["timeon"],
    "editFont": ["font"],
    "editMsgOff": ["editoff"],
    "editMsgOn": ["editon"],
    "setTime": ["settime"]
}

DEFAULT_FONT = "₀₁₂₃₄₅₆₇₈₉:"

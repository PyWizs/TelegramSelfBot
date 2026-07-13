from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


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
    "setTime": ["settime"],
    "lang": ["lang"],
    "translang": ["translang"],
    "translator": ["trans", "translate", "t"]
}

DEFAULT_FONT = "₀₁₂₃₄₅₆₇₈₉:"

# by Eldar Khuzin 20220824
import json

constants = {
    # Telegram API constants
    'TG_BOT_TOKEN': '',
    'TG_BOT_CHAT_ID': '',
    'TG_BOT_CHAT_LINK': '',

    # VK API constants
    'VK_ACCESS_TOKEN': '',
    'VK_API_VERSION': '',
    'VK_COUNT_VALUE': '',
}

WAIT_IN_RESPONSE_WHEEL = 4

def init():
    """
    Load constants dict
    """
    with open('constants.json', 'r') as file:
        global constants
        constants = json.load(file)

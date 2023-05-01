# by Eldar Khuzin 20220824
import json

constants = {
    # TG API constants
    'TG_BOT_TOKEN': '<your_bot_api_token>',
    'TG_BOT_CHAT_ID': '<chat_id_for_bot>',
    'TG_BOT_CHAT_LINK': '<chat_link_for_generate_reposts_links>',

    # VK API constants
    'VK_ACCESS_TOKEN': '<your_vk_app_access_token>',
    'VK_API_VERSION': '5.131',
    'VK_COUNT_VALUE': 4,
}

with open('constants.json', 'w') as file:
    json.dump(constants, file)

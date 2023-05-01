# by Eldar Khuzin 20220824
import time

import requests

import src.Constants as Const
import src.Communities as Comm
from src.VKapi import VK
from src.Bot import TelegramBot
from src.Database import db

# Load data
Const.init()
Comm.init()

# create main objects.
bt = TelegramBot()
vk = VK()


# handle post
def post_handle(title, post):
    time.sleep(10)
    try:
        # check copy history
        tg_id = False
        if 'copy_history' in post:
            for t in post['copy_history']:
                temp_post = vk.get_wall_post(t['owner_id'], t['id'])
                r = vk.get_group(t['owner_id'])
                Comm.communities[r['name']] = r['screen_name']
                temp_title = r['name']
                post_handle(temp_title, temp_post)
                tg_id = db.get_tg_id(t['id'])

        # send_post
        r = bt.send_post(title, post, tg_id)
        # add to db
        if (r['ok']):
            db.add_article_to_db(
                post['id'], r["result"]["message_id"], post['date'])
        else:
            with open('log.txt', 'a', encoding="UTF-8") as file:
                psid = post['id']
                log_mes = f'__ERROR__\n{str(title)}\n{str(psid)}\n'
                file.write(log_mes)
                file.write(f'{r}\n')
    except:
        pass


def spin():
    """
    Rotate feeds array
    """
    posts = []
    for title, domain in Comm.communities.items():
        time.sleep(Const.WAIT_IN_RESPONSE_WHEEL)  # wait for DDOS
        try:
            for post in vk.get_wall(domain, Const.constants['VK_COUNT_VALUE']):
                if db.article_is_not_db(post['id']):
                    posts.append((post['date'], title, post))
        except:
            pass

    posts.sort()
    for date, title, post in posts:
        post_handle(title, post)


# Runner :)
if __name__ == '__main__':
    spin()

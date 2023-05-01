# Bot support
import json
import requests
import urllib
import src.Constants as Const
import src.Communities as Comm

VK_LINK = 'https://vk.com/'
TG_API_LINK = 'https://api.telegram.org/bot'


def gen_link(link: str, text: str) -> str:
    """
    Create html style link
    """
    return f'<a href="{link}">{text}</a>'


def is_link(text) -> bool:
    """
    Simple link test for VK md text
    """
    if len(text) >= 4:
        return text[:4] == 'http'
    return False


def create_hashtag(text: str) -> str:
    """
    Generate hash tag for message.
    """
    for i in range(len(text)):
        if not (text[i].isalpha() or text[i].isdigit()):
            text = text.replace(text[i], ' ')
    return '#' + '_'.join(text.split())


def create_post_title(title: str) -> str:
    """
    Generate post title.
    """
    tag = create_hashtag(title)
    return f'<b>{title}</b>\n' + tag + '\n\n'


def isArticle(link: str) -> bool:
    """
    Validate is the given link is link to article.
    """
    return 'm.vk.com/@' in link


class TelegramBot:
    """
    Simple Telegram bot class.
    """

    def __doGET(self, cmd: str, params: dict = {}):
        """
        Do forse get response.
        """
        responce = requests.get(self.__BOT_URL + cmd, params=params)
        return json.loads(urllib.parse.unquote(responce.content))

    def __init__(self) -> None:
        self.__BOT_URL = TG_API_LINK + Const.constants['TG_BOT_TOKEN'] + '/'

    def sendMessage(self, params: dict):
        """
        Send message by bot api params values.
        """
        return self.__doGET('sendMessage', params)

    def __sendVKArticle(self, title, post, tg_id) -> None:
        """
        Send VK article to users.
        """

        # Store docs from VK message.
        docs = []

        # Store article links from VK message.
        articles = []

        def reg_doc(o: dict) -> None:
            """
            Registator doc link for file send.
            """
            nonlocal docs
            docs.append((o['title'], o['url']))

        # Dictionary of function for dispare VK message attributes.
        att_handle = {
            'doc': reg_doc,
        }

        def work_with_att(att):
            """
            Dispare attrinbutes from VK message.
            """
            nonlocal mes_links
            type = att['type']
            o = att[type]
            if type in att_handle:
                att_handle[type](o)
            elif 'url' in o:
                if isArticle(o['url']):
                    articles.append((o['title'], o['url']))
                else:
                    nonlocal was_links
                    was_links = True
                    mes_links += gen_link(o['url'], o['title']
                                          if 'title' in o else 'NOTITLE') + '\n'

        def create_post_text(text: str) -> str:
            """
            Replace name links [id0000|Username] to clickable links
            """
            nonlocal mes
            a, b, c = text.find('['), text.find('|'), text.find(']')
            while a < b < c:
                subst = text[a:c + 1]
                if is_link(text[a + 1:b]):
                    link = text[a + 1:b]
                else:
                    link = VK_LINK + text[a + 1:b]
                name = text[b + 1:c]
                text = text.replace(subst, gen_link(link, name))
                a, b, c = text.find('['), text.find('|'), text.find(']')
            return text

        # Flag for checking that is it name.
        is_not_first_message = False

        def send_text(text):
            """
            Send message and set flag.
            """
            nonlocal is_not_first_message
            is_not_first_message = True
            return self.sendMessage({
                'chat_id': Const.constants['TG_BOT_CHAT_ID'],
                'text': text,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True,
                'disable_notification': is_not_first_message,
            })

        # Generate post
        mes_title = create_post_title(title)
        mes_text = create_post_text(post['text'])
        mes_repost = ''
        if tg_id:
            mes_repost = '\n' + \
                gen_link(Const.constants['TG_BOT_CHAT_LINK'] +
                         str(tg_id), "<b>tgРЕПОСТ</b>")

        mes_links = '\n\n' + '<b>LINKS:</b>' + '\n'

        # work with attachments
        was_links = False
        if 'attachments' in post:
            atts = post['attachments']
            for att in atts:
                work_with_att(att)
        if was_links:
            mes_links += '\n'

        # add vk reference
        mes_links += gen_link("https://vk.com/wall" + str(post['owner_id']) + '_' + str(
            post['id']), "ОРИГИНАЛ")
        mes = mes_title + mes_text + mes_repost + mes_links

        # send message
        while mes.find('\n\n\n') != -1:
            mes = mes.replace('\n\n\n', '\n\n')
        if len(mes) > 4096:
            responce = send_text(mes_title)
            if len(mes_text) > 4096:
                while mes_text and len(mes_text) > 4096:
                    idx = mes_text[:4096].rfind(' ')
                    send_text(mes_text[:idx])
                    mes_text = mes_text[idx:]
                if mes_text:
                    send_text(mes_text)
            else:
                responce = send_text(mes_text)
            send_text(mes_repost)
            send_text(mes_links)
        else:
            responce = send_text(mes)

        # send Article
        for title, link in articles:
            self.sendMessage({
                'chat_id': Const.constants['TG_BOT_CHAT_ID'],
                'text': gen_link(link, title),
                'parse_mode': 'HTML',
                'disable_notification': True,
            })

        # send documents:
        for title, url in docs:
            tr = requests.get(url)
            requests.post(self.__BOT_URL + 'sendDocument',
                          params={
                              'chat_id': Const.constants['TG_BOT_CHAT_ID'],
                              'document': f'attach://{title}',
                              'disable_notification': True,
                          },
                          files={
                              title: tr.content
                          })
        return responce

    def send_post(self, title, post, tg_id=False):
        return self.__sendVKArticle(title, post, tg_id)

# by Eldar Khuzin 20220824
import json
import requests
import urllib
import src.Constants as Const


class VK:
    def doGET(self, cmd: str, params: dict = {}):
        """
        Do VK get
        """
        params.update(
            {'access_token': Const.constants['VK_ACCESS_TOKEN'], 'v': Const.constants['VK_API_VERSION']})
        r = requests.get(self.__VK_URL + cmd, params=params)
        return json.loads(urllib.parse.unquote(r.content))

    def __init__(self):
        self.__VK_URL = 'https://api.vk.com/method/'

    def get_wall(self, domain: str, count: int):
        """
        Get VK Wall.
        """
        return self.doGET('wall.get', {
            'filter': 'owner',
            'count': count,
            'domain': domain
        })['response']['items']

    def get_wall_post(self, owner_id, post_id):
        """
        Get VK Wall post.
        """
        return self.doGET('wall.getById', {
            'posts': f"{owner_id}_{post_id}",
        })['response'][0]

    def get_group(self, group_id):
        """
        Get VK group name
        """
        group_id = int(group_id)
        if group_id < 0:
            group_id = -group_id
        return self.doGET('groups.getById', {
            'group_id': group_id,
        })['response'][0]

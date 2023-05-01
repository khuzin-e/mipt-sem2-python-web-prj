# by Eldar Khuzin 20220824
import json

communities = dict()


def init():
    """
    Load communities dict
    """
    global communities
    with open('communities.json', 'r') as file:
        communities = json.load(file)

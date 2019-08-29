import giphy_client
import time
from pprint import pprint
import sys

from giphy_client.rest import ApiException

class Giphy():

    def __init__(self):
        self.api_instance = giphy_client.DefaultApi()
        self.api_key = 'dc6zaTOxFJmzC'
        # self.api_key = 'ds0sFJ0NPG0p84pFPBPo7HDXGorgI6C8'
        self.limit = 25
        self.offset = 0
        self.rating = 'g'
        self.lang = 'en'
        self.fmt = 'json'
    def getGifs(self, q):
        try:
            q = 'cheeseburger'
            api_response = self.api_instance.gifs_search_get(self.api_key, q, limit=self.limit, offset=self.offset, rating=self.rating, lang=self.lang, fmt=self.fmt)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


        return api_response


if __name__ == '__main__':
    g = Giphy()
    if len(sys.argv) > 1:
        res = g.getGifs(sys.argv[1])
    else:
        q = 'pikachu'
        res = g.getGifs(q)
    pprint(res)

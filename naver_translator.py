# -*- coding: utf-8 -*-
import os
import sys
import requests

class Translator():

    def __init__(self):

        self.client_id = "v6feWh_dn3A26cL4wB4K"
        self.client_secret = "FW4suGrz8J"

        encText = "나는 오늘 삼겹살과 피자를 맛있게 먹었다"
        payload = {"source" : 'ko', "target":"en", "text": encText}
        headers = {"X-Naver-Client-Id" : self.client_id, "X-Naver-Client-Secret": self.client_secret}
        url = "https://openapi.naver.com/v1/language/translate"

        res = requests.get(url, params=payload)
        print res

if __name__ == '__main__':
    t = Translator()

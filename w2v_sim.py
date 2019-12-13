# -*- coding: utf-8 -*-

import time
import sys
import os
from aurochs.buffalo import feature
from aurochs.misc import Aux
import json
import requests


class W2V():
    def __init__(self):
        self.logger = Aux.get_logger('w2v')
        self.key = None
        self.num = 100000
        self.d = '512d'

        self.topic = 'unified-buffalo-' + self.d
        self.name = 'w2v_' + self.d
        self.save_path = './' + self.name + '/'
        self.emojis = None
        self.custom_emojis = None
        self.sims_with_keyword = None
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        self.ft = None

        self.topn = 3
        self.threshold = 10.0
        self.load_model()

    def load_model(self):
        # get emoji list
        if not self.emojis:
            self.emojis = requests.get('https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json').json()

        # get custom emoji list (used in kakao-recoteam slack)
        if not self.custom_emojis:
            self.custom_emojis = requests.get('https://slack.com/api/emoji.list?token=xoxb-9983699043-717460665509-LvJsTUCLSHeHeZGIAnC5K79E').json()

        self.emojis = {each['short_name']: each['short_name'] for each in self.emojis}
        self.custom_emojis = self.custom_emojis['emoji']
        self.custom_emojis = {k: k for k in self.custom_emojis.keys()}
        # emoji + custom_emoji
        self.emojis.update(self.custom_emojis)

        # download word2vec model
        if not os.path.isfile(self.save_path + 'main'):
            os.system('ModelHouse export word2vec ' + self.topic + ' ' + self.save_path)

        # load w2v model
        self.ft = feature.load(self.save_path + 'main')

    def load_json(self, recs):
        fname = self.save_path + self.key + '.json'
        if os.path.isfile(fname):
            if os.path.getsize(fname) > 10:
                with open(self.save_path + self.key + '.json', 'r') as f:
                    self.sims_with_keyword = json.load(f)
                    if not self.sims_with_keyword:
                        return False
            else:
                os.remove(fname)

        self.logger.debug(self.key)
        # self.key shouldn't be unicode
        self.sims_with_keyword = self.ft.most_similar(self.key, self.num)
        if len(self.sims_with_keyword) > 0:
            self.logger.debug(self.sims_with_keyword[0])
        else:
            self.logger.debug(self.sims_with_keyword)
        self.sims_with_keyword = {kv[0].decode('utf-8'): kv[1] for kv in self.sims_with_keyword}
        with open(self.save_path + self.key + '.json', 'w') as f:
            json.dump(self.sims_with_keyword, f)

        return True

    def get_sim_emoji(self, keyword):

        self.logger.debug(type(keyword))

        # if alreay exists

        if isinstance(keyword, unicode):
            # unicode -> utf-8
            keyword = keyword.encode('utf-8')
        self.logger.debug(type(keyword))

        self.key = keyword
        recs = []
        j = self.load_json(recs)
        if not j:
            return ''
        if recs:
            return recs

        self.key = self.key.decode('utf-8')
        recs = []
        if self.emojis.get(self.key):
            recs.append((self.key, self.emojis.get(self.key), max(self.sims_with_keyword.values() if self.sims_with_keyword.values() else [0]) + 1.0))
        for emoji in self.emojis.keys():
            sim = self.sims_with_keyword.get(emoji)
            if sim and sim > self.threshold:
                recs.append((self.key, emoji, sim))
        self.logger.debug(recs[:2])
        if recs:
            recs = sorted(recs, key=lambda x: x[2], reverse=True)
        for i in recs[:self.topn]:
            self.logger.debug('[in recs] keyword : %s, emoji : %s, similarity : %.3f' % (i[0], i[1], i[2]))

        self.sims_with_keyword = sorted([(k, v) for k, v in self.sims_with_keyword.iteritems()], key=lambda x: x[1], reverse=True)

        for k, v in self.sims_with_keyword[:self.topn]:
            self.logger.debug('[in self.sims_with_keyword] word : %s, similarity : %.3f' % (k, v))
            # print item[0]
        if len(recs) > 0:
            # [(k, e, s), (k, e, s), ...]
            return recs[:self.topn]
        else:
            # []
            return recs
if __name__ == '__main__':
    w2v = W2V()
    print(sys.argv[1])
    res = w2v.get_sim_emoji(sys.argv[1])

# -*- coding: utf-8 -*-

from FE import FE
from w2v_sim import W2V
from aurochs.misc import Aux
from pprint import PrettyPrinter
from slackclient import SlackClient
from google_translator import Translator

import time
import random
import json

class Bot():
    def __init__(self):

        self.pp = PrettyPrinter()
        self.logger = Aux.get_logger("bot")
        # self.logger.debug = lambda x: self.logger.debug(self.pp.pformat(x)/
        self.bot_token = "xoxb-710178628226-723981424945-I8nqRBYzFyv9UoOTC9h9KOTY"
        # searchdog id
        self.bot_id = "BM9TLPGHJ"
        self.w2v = W2V()
        self.fe = FE()
        self.sc = SlackClient(self.bot_token)
        self.sc.rtm_connect()
        self.tc = Translator()

        self.threshold = 10.0
        self.topn = 1
        self.counter = 0

    def run(self):
        while True:
            rtm_output = self.sc.rtm_read()
            if rtm_output:
                if len(rtm_output) > 0:
                    if not rtm_output[0].get('name') == 'emoji_use':
                        self.logger.debug(rtm_output)
                    rtm_output = rtm_output[0]
            else:
                time.sleep(0.2)
                continue

            message = rtm_output.get('text', str())
            if rtm_output.get('bot_id', None) != self.bot_id and len(message) > 0:
                # if message : 김치돈가스뚝배기카레맛
                feats = self.fe.single_message_extract(rtm_output)
                # feats == (id, [term1, term2, ...])
                sim_emoji = []
                if feats:
                    t = time.time()
                    for feat in feats[1]:
                        # [김치, 돈가스, 뚝배기, 카레]
                        top_emojis= self.w2v.get_sim_emoji(feat)
                        top_emoji = top_emojis[:self.topn]
                        # [(feat, emoji, similarity), (feat, emoji, sim), ...]
                        self.logger.debug(top_emoji)
                        sim_emoji.extend(top_emoji)
                    self.logger.debug("time passed : %.2fs" % (time.time() - t))
                else:
                    # 김치돈가스뚝배기카레맛
                    top_emojis = self.w2v.get_sim_emoji(message)
                    top_emoji = top_emojis[:self.topn]
                    # [(feat, emoji, similarity), (feat, emoji, sim), ...]
                    self.logger.debug(top_emoji)
                    sim_emoji.extend(top_emoji)

                if sim_emoji:
                    random.shuffle(sim_emoji)
                    for t in sim_emoji:
                        self.logger.debug("%s -> %s : %.3f"%(t[0], t[1], t[2]))
                    out_num = 3
                    for reaction_tuple in sim_emoji[:out_num+1]:
                        feat, emoji, sim = reaction_tuple
                        self.logger.debug("(feat -> emoji) : (%s -> %s), similariy : %.3f"%(feat, emoji, sim))
                        res = self.sc.api_call(
                            "reactions.add",
                            channel = rtm_output.get('channel'),
                            name = emoji,
                            timestamp = rtm_output.get("ts")
                        )
                        if not res.get('ok'):
                            self.logger.debug(res)
            time.sleep(0.2)

if __name__ == "__main__":
    bot = Bot()
    bot.run()

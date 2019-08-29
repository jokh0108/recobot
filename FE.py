# -*- coding: utf-8 -*-
import sys
import json

from pprint import pprint

from aurochs.misc import Aux
from aurochs.vectorspace import IndexTerms

class FE:

    def __init__(self):

        self.logger = Aux.get_logger('FE')
        self.fe = IndexTerms('slack_messages')
        self.messages = None

    def load_model(self):
        with open('reaction_history.json') as json_file:
            self.messages = json.load(json_file)
        for k, v in self.messages.iteritems():
            print k, v

    def run(self):
        self.load_model()
        i = 0
        for m, r in self.messages.iteritems():
            print m
            messages_terms = self.fe.extract_index_term(i, m)
            i += 1
            if messages_terms[1]:
                for feat in messages_terms[1]:
                    print feat

            print '-'*50

    def single_message_extract(self, message):
        msg_id = message.get('client_msg_id')
        m = message.get('text').lower()
        if not m:
            return False
        message_terms = self.fe.extract_index_term(msg_id, m)
        # (id, [term1, term2, term3, ...])
        self.logger.debug(message_terms)
        if message_terms[1] and len(message_terms[1]) > 0:
            self.logger.debug("feat : %s" % (",".join(message_terms[1])))
            return message_terms
        else:
            return False


if __name__ == '__main__':
    fe = FE()

    if sys.argv[1]:
        message = {'client_msg_id': 1, 'text': sys.argv[1]}
        fe.single_message_extract(message)
    else:
        fe.run()

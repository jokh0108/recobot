# Imports the Google Cloud client library
from google.cloud import translate
from aurochs.misc import Aux


class Translator:

    def __init__(self):
        self.translate_client = translate.Client.from_service_account_json('/daum/oscar/recobot-test/google-cloud-auth.json')
        self.logger = Aux.get_logger('Translator')

    def translate(self, text= 'Hello World!', target= 'en'):

        # Translates some text into Russian
        translation = self.translate_client.translate(
            text,
            target_language=target)

        self.logger.debug(u'Text: {}'.format(text))
        self.logger.debug(u'Translation: {}'.format(translation['translatedText']))

        return translation['translatedText']

if __name__ =='__main__':
    t = Translator()
    t.translate()

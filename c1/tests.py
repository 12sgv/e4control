from otree.api import Bot
from . import *

#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        #instructions app
        # Enter 'bot' in the prolificID field and submit the page
        yield c11, dict(prolificID='bot')
        yield c12
        yield c13
        yield c14

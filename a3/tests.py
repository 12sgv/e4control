from otree.api import Bot
from . import *

#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.participant.vars['r23']==True:
            yield a32
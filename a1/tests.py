from otree.api import Bot
from . import *

#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        #instructions app
        # Enter 'bot' in the prolificID field and submit the page
        yield a11, dict(prolificID='bot')
        yield a12
        yield a13
        yield a14
        choices = ['Remote']*60 + ['Hybrid']*40
        vote = random.choice(choices)
        yield a15, dict(policy_vote=vote)
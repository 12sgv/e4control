from otree.api import Bot
from . import *

#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        #instructions app
        # Enter 'bot' in the prolificID field and submit the page
        yield ProlificID, dict(prolificID='bot')
        yield Consent
        yield GeneralInstructions
        yield Overview
        choices = ['Remote']*86 + ['Office']*14
        vote = random.choice(choices)
        yield Voting, dict(policy_vote=vote)
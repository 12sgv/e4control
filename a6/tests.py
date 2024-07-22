from otree.api import Bot
from . import *


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        # payment_info app
        if self.participant.vars['is_out'] == False and self.participant.vars['timed_out'] == False:
            yield a61
        elif self.participant.vars['is_out'] == True:
            yield a62
        elif self.participant.vars['group_formation_timeout'] == 1:
            yield a63
        elif self.participant.vars['kicked_out'] == 1:
            yield a64
        if not self.participant.vars['kicked_out'] == 1:
            yield Submission(a65, dict(feedback='bot'), check_html=False)
            yield Submission(a66, check_html=False)


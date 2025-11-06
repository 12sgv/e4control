from otree.api import Bot
from . import *


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        # payment_info app
        if self.participant.vars['is_out'] == False and self.participant.vars['timed_out'] == False:
            yield a51
        elif self.participant.vars['group_formation_timeout'] == 1:
            yield a52
        elif self.participant.vars['kicked_out'] == 1:
            yield a53
        if not self.participant.vars['kicked_out'] == 1:
            yield Submission(a54, dict(feedback='bot'), check_html=False)
        if not self.participant.vars['kicked_out'] == 1:
            yield Submission(a55, check_html=False)


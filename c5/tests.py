from otree.api import Bot
from . import *


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        # payment_info app
        if self.player.participant.vars['not_paired'] == False and self.player.participant.vars['timed_out'] == False:
            yield c51
        if self.player.participant.vars['not_paired'] == True:
            yield c52
        if self.participant.vars['group_formation_timeout'] == True:
            yield c53
        if self.participant.vars['kicked_out'] == True:
            yield c54
        else:
            yield Submission(c55, dict(feedback='bot'), check_html=False)
            yield Submission(c56, check_html=False)


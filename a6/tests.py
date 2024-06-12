from otree.api import Bot
from . import *


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        # payment_info app
        if self.player.participant.vars['is_out'] == False and self.player.participant.vars['timed_out'] == False:
            yield ResultsComplete
        if self.player.participant.vars['is_out'] == True:
            yield ResultsNotPaired
        if self.participant.vars['timed_out'] == True:
            yield ResultsTimedOut
        if self.participant.vars['timed_out'] == False:
            yield Submission(PaymentInfo, dict(feedback='bot'), check_html=False)


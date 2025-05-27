from otree.api import Bot
from . import *
import random


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if not self.participant.vars['is_out'] and not self.player.participant.vars['timed_out']:
            # survey app
            #generate random choices for Demo 1
            em = random.randint(1, 3)
            wl = random.randint(1, 4)
            lp = random.randint(1, 4)
            ed = random.randint(1, 6)
            we = random.randint(0, 80)
            fai_choices = ['Yes']*67 + ['No']*33
            fai = random.choice(fai_choices)
            rai_choices = ['Yes'] * 67 + ['No'] * 33
            rai = random.choice(fai_choices)
            # On the Demographics1 page, enter the specified values and submit the page
            yield a51, dict(
                employed=em,
                work_location=wl,
                location_preference=lp,
                education=ed,
                work_experience=we,
                firm_allow_input=fai,
                remote_allow_input=rai,
            )
from otree.api import Bot
from . import *
import random


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['is_out'] == False:
            # survey app
            #generate random responses
            vp = random.randint(-3, 3)
            vv = random.randint(-3, 3)
            a = random.randint(-3, 3)
            ii = random.randint(-3, 3)
            ih = random.randint(-3, 3)
            il = random.randint(-3, 3)
            b = random.randint(0, 6)
            s = random.randint(0, 6)
            expectation_choices = ['Remote'] * 86 + ['Office'] * 14
            ev = random.choice(expectation_choices)
            es = random.randint(-3, 3)
            # On the PEQ page, enter the specified values and submit the page
            yield PEQ, dict(
                vote_preference=vp,
                vote_valued=vv,
                affect=a,
                identity_identify=ii,
                identity_happy=ih,
                identity_like=il,
                blame=b,
                sympathy=s,
                expectation_valence=ev,
                expectation_strength=es,
            )

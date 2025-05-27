from otree.api import Bot
from . import *
import random


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.participant.vars['is_out'] == False:
            # survey app
            #generate random responses
            vp = random.randint(0, 6)
            a = random.randint(-3, 3)
            vf = random.randint(-3, 3)
            ii = random.randint(-3, 3)
            ih = random.randint(-3, 3)
            il = random.randint(-3, 3)
            b = random.randint(0, 6)
            s = random.randint(0, 6)
            d = random.randint(0, 6)
            fh = random.randint(-3, 3)
            eq = random.randint(-3, 3)
            expectation_choices = ['Remote'] * 58 + ['Hybrid'] * 38 + ['None'] * 4
            ev = random.choice(expectation_choices)
            es = random.randint(-3, 3)
            # On the PEQ page, enter the specified values and submit the page
            yield a42, dict(
                vote_preference=vp,
                affect=a,
                vote_fair=vf,
                identity_identify=ii,
                identity_happy=ih,
                identity_like=il,
                blame=b,
                sympathy=s,
                deserving=d,
                fair_help=fh,
                equality=eq,
                expectation_valence=ev,
                expectation_strength=es,
            )

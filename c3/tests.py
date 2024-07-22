from otree.api import Bot
from . import *
import random


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['not_paired'] == False:
            #identity PEQ
            ii = random.randint(-3, 3)
            ih = random.randint(-3, 3)
            il = random.randint(-3, 3)
            yield c32, dict(
                identity_identify=ii,
                identity_happy=ih,
                identity_like=il,
            )
            #Voting page
            choices = ['Remote'] * 86 + ['Office'] * 14
            vote = random.choice(choices)
            yield c33, dict(policy_vote=vote)
            #Voting PEQ

            # survey app
            #generate random responses
            vp = random.randint(-3, 3)
            vv = random.randint(-3, 3)
            expectation_choices = ['Remote'] * 86 + ['Office'] * 14
            ev = random.choice(expectation_choices)
            es = random.randint(-3, 3)
            # On the PEQ page, enter the specified values and submit the page
            yield c34, dict(
                vote_preference=vp,
                vote_valued=vv,
                expectation_valence=ev,
                expectation_strength=es,
            )

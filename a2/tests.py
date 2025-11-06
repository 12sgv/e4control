from . import *
import random

#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        yield Submission(a22, check_html=False)
        #for main group
        if not self.participant.vars['is_out'] == 1:
            yield a23
            #get vars for a24
            help = random.randrange(0, 61, 5)
            #Check that the wrong answers are, in fact, wrong
            yield Submission(a24,  {'helping': help}, check_html=False)
            #a31 is a wait page
            yield Submission(a32, check_html=False)
            yield a33
            #HERE IS WHERE PEQ STARTS
            #a34
            id1 = random.randint(-3, 3)
            id2 = random.randint(-3, 3)
            id3 = random.randint(-3, 3)
            deserve = random.randint(0, 6)
            fair = random.randint(-3, 3)
            cost = random.randint(-3, 3)
            yield a34, dict(
                identity_identify = id1,
                identity_happy = id2,
                identity_like = id3,
                fair_help = fair,
                deserving = deserve,
                equality = cost,
            )
            #a35
            choices = ['Remote'] * 60 + ['Hybrid'] * 40
            vote = random.choice(choices)
            yield a35, dict(policy_vote=vote)
            #a36
            vp = random.randint(0, 6)
            expectation_choices = ['Remote'] * 58 + ['Hybrid'] * 38 + ['None'] * 4
            ev = random.choice(expectation_choices)
            es = random.randint(-3, 3)
            yield a36, dict(
                vote_preference = vp,
                expectation_valence = ev,
                expectation_strength = es,
            )

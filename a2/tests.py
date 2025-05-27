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
            if self.player.participant.vars['treatment'] == 1:
                wrong1 = 4
                wrong2 = 2
                wrong3 = 3
                manipulation_answer = 1
            elif self.player.participant.vars['treatment'] == 2:
                wrong1 = 1
                wrong2 = 4
                wrong3 = 3
                manipulation_answer = 2
            elif self.player.participant.vars['treatment'] == 3:
                wrong1 = 1
                wrong2 = 2
                wrong3 = 4
                manipulation_answer = 3
            else:
                wrong1 = 1
                wrong2 = 2
                wrong3 = 3
                manipulation_answer = 4
            #Check that the wrong answers are, in fact, wrong
            yield SubmissionMustFail(a24, dict(partner_check=wrong1))
            yield SubmissionMustFail(a24, dict(partner_check=wrong2))
            yield SubmissionMustFail(a24, dict(partner_check=wrong3))
            yield a24, dict(partner_check=manipulation_answer)
            #vars for a25
            offer = random.choice(range(0, 65, 5))  # Picks a random number from 0 to 60 in increments of 5
            yield Submission(a25, {'helping': offer}, check_html=False)

        #for 5th person
        if self.participant.vars['not_paired'] == 1:
            yield a26


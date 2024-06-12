from . import *


#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['is_out'] == False:
            yield Submission(NoGroup, check_html=False)
            yield VoteOutcome
            if self.player.participant.vars['treatment'] == 1:
                manipulation_answer = 1
            elif self.player.participant.vars['treatment'] == 2:
                manipulation_answer = 2
            elif self.player.participant.vars['treatment'] == 3:
                manipulation_answer = 3
            else:
                manipulation_answer = 4
            yield PartnerCheck, dict(partner_check=manipulation_answer)
            offer = random.randint(0, 100)
            yield Submission(Offer, {'giving': offer}, check_html=False)

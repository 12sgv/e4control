from . import *


#this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['group_formation_timeout'] == False:
            yield Submission(c22, check_html=False)
            if self.player.participant.vars['not_paired'] == False:
                yield c23
                offer = random.randint(0, 100)
                yield Submission(c24, {'giving': offer}, check_html=False)

            else:
                yield c25



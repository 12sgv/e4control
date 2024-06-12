from otree.api import Bot
from . import *
import random


# this bot plays through correctly (complete)
class PlayerBot(Bot):
    def play_round(self):
        if self.player.participant.vars['timed_out'] == False:
            # survey app
            #generate random choices for Demo 1
            em = random.randint(1, 4)
            wl = random.randint(1, 5)
            lp = random.randint(1, 5)
            ts = random.randint(1, 5)
            ind = random.randint(1, 8)
            ed = random.randint(1, 6)
            we = random.randint(0, 80)
            fai_choices = ['Yes']*67 + ['No']*33
            fai = random.choice(fai_choices)
            # On the Demographics1 page, enter the specified values and submit the page
            yield Demographics1, dict(
                employed=em,
                work_location=wl,
                location_preference=lp,
                team_size=ts,
                industry=ind,
                education=ed,
                work_experience=we,
                firm_allow_input=fai,
            )
            if self.player.participant.vars['firm_allow_input'] == True:
                # On the Demographics2 page, enter the specified values and submit the page
                fi = random.randint(1, 6)
                ffi = random.randint(1, 7)
                ffrp_choices = ['Yes'] + ['No']
                ffrp = random.choices(ffrp_choices)
                fapp = random.randint(1, 4)
                yield Demographics2, dict(
                    firm_input=fi,
                    firm_input_other="bot is here",
                    firm_feel_input=ffi,
                    firm_full_remote_pandemic=ffrp,
                    firm_adjust_post_pandemic=fapp,
                )
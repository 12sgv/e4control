from otree.api import *
from otree.export import get_fields_for_csv
import random
import time

doc = """
2/3 REMOTE
App 3/6 in sequence.
App Before: a1 (Intro)
App After: a5 (Survey)
---------------------------------------
After voting, 2/3 of the Remote participants are directed to this app.
This app includes the wait page and additional instructions for the 2/3 Remote participants.
They wait at the wait page and upon a team of 5 2/3 Remote participants arrives.
Then, participants learn they are in the shortened version of the study and advance to the survey (a5).
"""


class C(BaseConstants):
    NAME_IN_URL = 'a3'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = 5


class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= self.session.config['group_size']:
            return waiting_players[:self.session.config['group_size']]
        # timeout the participants who don't get placed into a group in time.
        for player in waiting_players:
            if waiting_too_long_group_formation(player):
                player.participant.vars['group_formation_timeout'] = 1
                player.participant.vars['pair_number'] = 97
                return [player]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # page vars
    remote_group_formation_timeout = models.BooleanField(initial=False)


# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']


# PAGES
#6b. Team Advancement Page (2/3 Remote
class a31(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'Your vote has been recorded. You will automatically advance to the next page when all members ' \
                'of your team are ready to advance.'

    # timeout those who are waiting too long on this page and pay them the basic fee
    def before_next_page(self, timeout_happened):
        if timeout_happened:
            self.remote_group_formation_timeout = True
            self.participant.vars['remote_group_formation_timeout'] = True


#Further Instruction page for 2/3 Remote
class a32(Page):
    # send everyone after this to the survey page
    def app_after_this_page(self, upcoming_apps):
        return "a5"

page_sequence = [a31, a32]

from otree.api import *
from otree.export import get_fields_for_csv
import random
import time

doc = """
INSTRUCTIONS
App 1/5 in sequence.
App Before: None [Prolific]
App After: c2 (Helping Task)
---------------------------------------
Participants are directed to this app from Prolific via a link on Prolific.
In this app, participants give consent, input ProlificID, read instructions, and then read background information.
After advancing, participants move to the main part of the study (c2).
"""


class C(BaseConstants):
    NAME_IN_URL = 'c1'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = 5


class Subsession(BaseSubsession):
    pass


def creating_session(self):
    print("creating session called")
    session = self.session
    # initialize counters for the conditions and for the partner list
    session.vars['num_winner_winner_pairs'] = 0
    session.vars['num_winner_loser_pairs'] = 0
    session.vars['num_loser_loser_pairs'] = 0
    session.vars['group_number'] = 1
    session.vars['group_type'] = 1
    session.vars['partner_list'] = []
    #for Control
    session.vars['paired_group'] = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolificID = models.StringField(label='To continue, please input your Prolific ID.')
    control = models.BooleanField(initial=False)
    # 2/3 Remote Var
    r23 = models.BooleanField(initial=False)
    # initialize variables used throughout the study
    is_out = models.BooleanField(initial=False)
    not_paired = models.BooleanField()
    # timed out vars
    timed_out = models.BooleanField(initial=False)
    timed_out_vote = models.BooleanField(initial=False)
    finished_voting = models.BooleanField(initial=False)
    timed_out_vote_outcome = models.BooleanField(initial=False)
    finished_vote_outcome = models.BooleanField(initial=False)
    group_formation_timeout = models.BooleanField()
    timed_out_help = models.BooleanField()
    # pairing vars
    pair_number = models.IntegerField()
    new_group_identifier = models.IntegerField(initial=0)
    earnings = models.CurrencyField(initial=0)


# PAGES
#1. Prolific ID
class c11(Page):
    def is_displayed(self):
        return not hasattr(self, 'label') or not self.prolificID

    form_model = 'player'
    form_fields = ['prolificID']

    def vars_for_template(self):
        self.participant.vars['timed_out_vote'] = False

    # record prolificID and ip address for the next apps
    def before_next_page(self, timeout_happened):
        self.participant.label = self.prolificID
        self.participant.vars['prolificID'] = self.prolificID
        self.control = True
        self.participant.vars['control'] = True

#2. Consent
class c12(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'participation_fee': player.session.config['participation_fee']
        }

    # pass initialized variables to the rest of the apps
    def before_next_page(self, timeout_happened):
        self.participant.vars['finished_voting'] = False
        self.participant.vars['is_out'] = False
        self.participant.vars['not_paired'] = False
        self.participant.vars['timed_out'] = False
        self.participant.vars['other_timed_out'] = False
        self.participant.vars['kicked_out'] = False
        self.participant.vars['timed_out_vote_outcome'] = False
        self.participant.vars['finished_vote_outcome'] = False
        self.participant.vars['timed_out_help'] = False
        self.participant.vars['pair_number'] = 99
        self.participant.vars['group_formation_timeout'] = False
        self.participant.vars['partner_check_incorrect_count'] = 0
        self.participant.vars['new_group_identifier'] = 0
        self.participant.vars['earnings'] = 0
        self.participant.vars['paired_group'] = 0
        if hasattr(self, 'label'):
            self.prolificID = self.participant.label
            self.participant.vars['prolificID'] = self.prolificID

#3. General Instructions
class c13(Page):
    pass

#4. Overview of Task
class c14(Page):
    def vars_for_template(self):
        return {
            'participation_fee': self.session.config['participation_fee']
        }

    def before_next_page(self, timeout_happened):
        self.participant.vars['group_formation_arrival'] = time.time()



page_sequence = [c11, c12, c13, c14]

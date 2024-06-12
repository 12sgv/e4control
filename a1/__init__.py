from otree.api import *
from otree.export import get_fields_for_csv
import random
import time

doc = """
INSTRUCTIONS
App 1/6 in sequence.
App Before: None
App After: help for completed participants or wait23 for 2/3 remote participants
---------------------------------------
Participants give consent, input ProlificID if it wasn't already grabbed, read instructions, read background, and vote.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a1'
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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolificID = models.StringField(label='To continue, please input your Prolific ID.')
    policy_vote = models.StringField(
        choices=[
            ['Office', 'Fully in-office policy'],
            ['Remote', 'Fully remote policy'],
        ],
        label='I vote for the:',
        widget=widgets.RadioSelect
    )
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
class ProlificID(Page):
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

    # js to grap the ip address using ipify
    def js_vars(self):
        return {
            'ipify_url': 'https://api.ipify.org?format=jsonp&callback=?'
        }


class Consent(Page):
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
        self.participant.vars['timed_out_vote_outcome'] = False
        self.participant.vars['finished_vote_outcome'] = False
        self.participant.vars['timed_out_help'] = False
        self.participant.vars['pair_number'] = 99
        self.participant.vars['group_formation_timeout'] = False
        self.participant.vars['partner_check_incorrect_count'] = 0
        self.participant.vars['new_group_identifier'] = 0
        self.participant.vars['earnings'] = 0
        if hasattr(self, 'label'):
            self.prolificID = self.participant.label
            self.participant.vars['prolificID'] = self.prolificID


class GeneralInstructions(Page):
    pass


class Overview(Page):
    def vars_for_template(self):
        return {
            'participation_fee': self.session.config['participation_fee']
        }


class Voting(Page):
    form_model = 'player'
    form_fields = ['policy_vote']

    def vars_for_template(self):
        return {
            'office': 'Office',
            'remote': 'Remote',
            'group_size': self.session.config['group_size'],
        }

    def before_next_page(self, timeout_happened):
        self.participant.vars['policy_vote'] = self.policy_vote
        self.finished_voting = True
        self.participant.vars['finished_voting'] = True
        self.participant.vars['group_formation_arrival'] = time.time()
        # kick out 2/3 of remote votes
        rand_num = random.randrange(0,100,1)
        print("Random Number:", rand_num)
        print("Cutoff:", self.session.config['remote_cutoff'])
        #Kick out the 2/3 remote voters
        if rand_num < self.session.config['remote_cutoff'] and self.policy_vote == "Remote":
            self.r23 = True
            self.participant.vars['r23'] = True
            self.is_out = True
            self.participant.vars['is_out'] = True

        #Send the rest of the participants to their own page
        else:
            self.participant.vars['r23'] = False
            self.participant.vars['not_paired'] = False

    # send 2/3 Remote to their own wait page
    def app_after_this_page(self, upcoming_apps):
        if self.r23 == True:
            return "wait23"



page_sequence = [ProlificID, Consent, GeneralInstructions, Overview, Voting]

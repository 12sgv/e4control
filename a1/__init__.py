from otree.api import *
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe
import random
import time

doc = """
INSTRUCTIONS
App 1/4 in sequence.
App Before: None [Prolific]
App After: a2 (Helping)
---------------------------------------
Participants are directed to this app from Prolific via a link on Prolific.
In this app, participants input ProlificID, consent to the study, read instructions, read an overview, and then
go to form their team., and then vote. Then participants advance to a2
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
    session.vars['group_number'] = 1
    session.vars['group_type'] = 1
    session.vars['partner_list'] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolificID = models.StringField(label='To continue, please input your Prolific ID.')
    # pairing vars
    group_number = models.IntegerField(initial=0)
    treatment = models.IntegerField(initial=40)
    #payoff  vars
    earnings = models.CurrencyField(initial=0)


# PAGES
#1. Prolific ID
class a11(Page):
    def is_displayed(self):
        return not hasattr(self, 'label') or not self.prolificID
    form_model = 'player'
    form_fields = ['prolificID']

    #initialize vars for rest of study
    def vars_for_template(self):
        self.participant.vars['group_number'] = 0
        self.participant.vars['treatment'] = self.treatment
        self.participant.vars['group_formation_timeout'] = False
        self.participant.vars['timed_out'] = False
        self.participant.vars['kicked_out'] = False
        self.participant.vars['is_out'] = False
        self.earnings = cu(self.session.config['participation_fee'] + self.session.config['initial_payoff_amount'])

    # record prolificID for the next apps
    def before_next_page(self, timeout_happened):
        self.participant.label = self.prolificID
        self.participant.vars['prolificID'] = self.prolificID

#2. Consent
class a12(Page):
    pass

#3. General Instructions
class a13(Page):
    pass

#4. Overview of Task
class a14(Page):
    def before_next_page(self, timeout_happened):
        self.participant.vars['group_formation_arrival'] = time.time()

page_sequence = [a11, a12, a13, a14]

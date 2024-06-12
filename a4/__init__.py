from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
App 4/6 in sequence.
App Before: help
App After: survey
---------------------------------------
Participants complete the PEQ
Participants complete the Demographics
"""


class C(BaseConstants):
    NAME_IN_URL = 'a3'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = None
    StandardChoices = [
        [-3, 'Strongly disagree'],
        [-2, 'Moderately disagree'],
        [-1, 'Slightly disagree'],
        [0, 'Neutral'],
        [1, 'Slightly agree'],
        [2, 'Moderately agree'],
        [3, 'Strongly agree'],
    ]
    AffectChoices = [
        [-3, 'Strongly negative'],
        [-2, 'Moderately negative'],
        [-1, 'Slightly negative'],
        [0, 'Indifferent'],
        [1, 'Slightly positive'],
        [2, 'Moderately positive'],
        [3, 'Strongly positive'],
    ]
    StandardChoiceTable = [
        'Strongly disagree',
        'Moderately disagree',
        'Slightly disagree',
        'Neutral',
        'Slightly agree',
        'Moderately agree',
        'Strongly agree',
    ]
    AffectChoiceTable = [
        'Strongly negative',
        'Moderately negative',
        'Slightly negative',
        'Indifferent',
        'Slightly positive',
        'Moderately positive',
        'Strongly positive',
    ]
    FeelChoiceTable = [
        'Not at all',
        '',
        '',
        '',
        '',
        '',
        'A great extent',
    ]

class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        #initialize a dictionary to hold the list of groups
        d = {}
        for player in waiting_players:
            group_id = player.participant.vars['group_number']
            if group_id not in d:
                d[group_id] = []
            players_in_my_group = d[group_id]
            players_in_my_group.append(player)
            if group_id > 0:
                if len(players_in_my_group) == 2:
                    return players_in_my_group

        #check if any player has been waiting too long
        for player in waiting_players:
            if waiting_too_long_partner_formation(player):
                print("player waiting too long. player:", player.id)
                return [player]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    is_out = models.BooleanField()
    is_bot = models.BooleanField()
    other_giving = models.IntegerField()
    # PEQ
    vote_preference = models.IntegerField(choices=C.StandardChoices,
                                          widget=widgets.RadioSelectHorizontal,
                                          label='I feel strongly about the policy I voted for.')
    vote_valued = models.IntegerField(choices=C.StandardChoices,
                                      widget=widgets.RadioSelectHorizontal,
                                      label='The company values employee input on their remote versus in-office work policy.')
    affect = models.IntegerField(choices=C.AffectChoices,
                                 widget=widgets.RadioSelect,
                                 label='How did you feel about the outcome of the vote? (i.e., whether you won or lost.)')
    identity_identify = models.IntegerField(choices=C.StandardChoices,
                                            widget=widgets.RadioSelect,
                                            label='I identify with my partner.')
    identity_happy = models.IntegerField(choices=C.StandardChoices,
                                         widget=widgets.RadioSelect,
                                         label='I feel happy to be paired with my partner.')
    identity_like = models.IntegerField(choices=C.StandardChoices,
                                        widget=widgets.RadioSelect,
                                        label='I like my partner.')
    blame = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, ''],
        [3, ''],
        [4, ''],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent were you angry or upset with your partner because of the outcome of the vote?')
    sympathy = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, ''],
        [3, ''],
        [4, ''],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent did you feel bad for your partner because of the outcome of the vote?')
    expectation_valence = models.StringField(
        choices=[
            ['Office', 'Fully in-office policy'],
            ['Remote', 'Fully remote policy'],
            ['None', "I didn't consider which policy would win"]
        ],
        widget=widgets.RadioSelect,
    )
    expectation_strength = models.IntegerField(choices=C.StandardChoices,
                                               widget=widgets.RadioSelectHorizontal,
                                               label="How confident were you that you would win the vote?")

#FUNCTIONS
# function to determine if waiting to long for the partner to arrive
def waiting_too_long_partner_formation(self):
    return time.time() - self.participant.vars['help_completion_time'] > self.session.config[
        'partner_creation_timeout']
# retrieve what other player provided
def other_giving(self):
    if self.id_in_group == 1:
        other_player = self.group.get_player_by_id(2)
    elif self.id_in_group == 2:
        other_player = self.group.get_player_by_id(1)
    else:
        print("no id in group for this player. Player group id:", self.id_in_group)
    self.participant.vars['other_giving'] = other_player.giving
    return self.participant.vars['other_giving']

# PAGES
class PartnerWait(WaitPage):
    group_by_arrival_time = True
    title_text = 'Help Completion Page'
    body_text = 'The amount of help you have given to your partner has been recorded and both of your payoffs' \
                ' have been adjusted accordingly. You will automatically advance to the next page shortly where ' \
                'you will answer a few survey questions about the study…'

    def after_all_players_arrive(self):
        for player in self.group.get_players():
            other_player = player.get_others_in_group()[0]
            #check if partner timed out
            if other_player.participant.vars['is_out'] == True:
                print("before other player is out TRUE")
                player.participant.vars['other_timed_out_help'] = True
                print("after other player is out TRUE")
            else:
                print("before other player is out FALSE")
                player.participant.vars['other_timed_out_help'] = False
                print("after other player is out FALSE")
                # calculate various payoff functions
            player.other_giving = other_player.participant.vars['giving']
            player.participant.vars['other_giving'] = player.other_giving

class PEQ(Page):
    form_model = 'player'
    form_fields = ['vote_preference', 'vote_valued', 'affect', 'identity_identify', 'identity_happy', 'identity_like', 'blame',
                   'sympathy', 'expectation_valence', 'expectation_strength']

    def vars_for_template(self):
        return dict(
        #expectation_strength_label = "How confident were you that the fully {} policy would win?".format(self.participant.vars['policy_vote'])
        )
 #   def is_displayed(self):
 #       if self.participant.vars['is_out'] == True:
 #           return False
 #       else:
 #           return True

page_sequence = [PartnerWait, PEQ]

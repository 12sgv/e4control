from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
App 3/6 in sequence.
App Before: help
App After: survey
---------------------------------------
Participants complete the PEQ
Participants complete the Demographics
"""


class C(BaseConstants):
    NAME_IN_URL = 'c3'
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
        l = {}
        for player in waiting_players:
            if player.participant.vars.get('other_timed_out', 0) == 1:
                return [player]
            group_id = player.participant.vars['paired_group']
            if group_id not in l:
                l[group_id] = []
            players_in_my_group = l[group_id]
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
    #timint vars
    finished_voting = models.BooleanField(initial=False)
    # PEQ Identity
    identity_identify = models.IntegerField(choices=C.StandardChoices,
                                            widget=widgets.RadioSelect,
                                            label='I identify with my partner.')
    identity_happy = models.IntegerField(choices=C.StandardChoices,
                                         widget=widgets.RadioSelect,
                                         label='I feel happy to be paired with my partner.')
    identity_like = models.IntegerField(choices=C.StandardChoices,
                                        widget=widgets.RadioSelect,
                                        label='I like my partner.')
    #Voting Field
    policy_vote = models.StringField(
        choices=[
            ['Office', 'Fully in-office policy'],
            ['Remote', 'Fully remote policy'],
        ],
        label='I would vote for the:',
        widget=widgets.RadioSelect
    )
    #PEQ Voting
    vote_preference = models.IntegerField(choices=C.StandardChoices,
                                          widget=widgets.RadioSelectHorizontal,
                                          label='I feel strongly about the policy I voted for.')
    vote_valued = models.IntegerField(choices=C.StandardChoices,
                                      widget=widgets.RadioSelectHorizontal,
                                      label='The company values employee input on their remote versus in-office work policy.')
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
                                               label="",
                                               blank=True)

#FUNCTIONS
# function to determine if waiting to long for the partner to arrive
def waiting_too_long_partner_formation(self):
    return time.time() - self.participant.vars['help_completion_time'] > self.session.config[
        'c_help_wait_timeout']
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
# 8. Help Completion Page
class c31(WaitPage):
    group_by_arrival_time = True
    title_text = 'Help Completion Page'
    body_text = 'The amount of help you have given to your partner has been recorded and both of your payoffs' \
                ' have been adjusted accordingly. You will automatically advance to the next page shortly…'

#9. Survey Questions about the Helping
class c32(Page):
    form_model = 'player'
    form_fields = ['identity_identify', 'identity_happy', 'identity_like']

    def vars_for_template(self):
        return dict(
        #expectation_strength_label = "How confident were you that the fully {} policy would win?".format(self.participant.vars['policy_vote'])
        )

    #pass other giving vars to player
    def vars_for_template(self):
        if self.participant.vars['other_timed_out'] == 0 and len(self.group.get_players())>1:
            if self.id_in_group == 1:
                other_player = self.group.get_player_by_id(2)
            elif self.id_in_group == 2:
                other_player = self.group.get_player_by_id(1)
            self.participant.vars['partner_session_id'] = other_player.participant.id_in_session
            self.other_giving = other_player.participant.vars['giving']
            self.participant.vars['other_giving'] = self.other_giving
        else:
            pass

#10. Voting
class c33(Page):
    form_model = 'player'
    form_fields = ['policy_vote']


    def before_next_page(self, timeout_happened):
        self.participant.vars['policy_vote'] = self.policy_vote
        self.finished_voting = True
        self.participant.vars['finished_voting'] = True

#11. PEQ Voting (Survey) for Main Group
class c34(Page):
    form_model = 'player'
    form_fields = ['vote_preference', 'vote_valued', 'expectation_valence', 'expectation_strength']

    def vars_for_template(self):
        return dict(
        #expectation_strength_label = "How confident were you that the fully {} policy would win?".format(self.participant.vars['policy_vote'])
        )

page_sequence = [c31, c32, c33, c34]

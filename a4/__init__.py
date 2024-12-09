from otree.api import *
import time
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe

doc = """
PEQ
App 4/6 in sequence.
App Before: a2 (Main Task)
App After: a5 (Survey)
---------------------------------------
Participants that are part of the main group advance to this page after completing the main experimental task (a2).
Participants answer PEQ questions bout their experience in the study.
Fifth participants view a modified version of the questions.
All participants advance to the survey (a5) after completing this app.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a4'
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
        'Slightly',
        '',
        'Moderately',
        '',
        'A great extent',
    ]
    ConfidenceTable = [
        'Not at all confident',
        '',
        'Slightly confident',
        '',
        'Moderately confident',
        '',
        'Extremely confident',
    ]
    PreferenceTable = [
        'No preference',
        '',
        'Slight preference',
        '',
        'Moderate preference',
        '',
        'Very strong preference',
    ]

class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        #initialize a dictionary to hold the list of groups
        d = {}
        for player in waiting_players:
            if player.participant.vars.get('other_timed_out', 0) == 1:
                return [player]
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
    vote_preference = models.IntegerField(choices=[
                                          [0, 'No preference'],
                                          [1, ''],
                                          [2, 'Slight preference'],
                                          [3, ''],
                                          [4, 'Moderate preference'],
                                          [5, ''],
                                          [6, 'Very strong preference']],
                                          widget=widgets.RadioSelectHorizontal,
                                          label='To what extent did you prefer the policy you voted for over the other policy?')
    affect = models.IntegerField(choices=C.AffectChoices,
                                 widget=widgets.RadioSelect,
                                 label='How did you feel about the outcome of the vote? (i.e., whether you won or lost)')
    identity_identify = models.IntegerField(choices=C.StandardChoices,
                                            widget=widgets.RadioSelect,
                                            label='I identified with my partner.')
    identity_happy = models.IntegerField(choices=C.StandardChoices,
                                         widget=widgets.RadioSelect,
                                         label='I was happy to be paired with my partner.')
    identity_like = models.IntegerField(choices=C.StandardChoices,
                                        widget=widgets.RadioSelect,
                                        label='I liked my partner.')
    blame = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, 'Slightly'],
        [3, ''],
        [4, 'Moderately'],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent were you angry or upset with your partner because of the outcome of the vote?')
    sympathy = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, 'Slightly'],
        [3, ''],
        [4, 'Moderately'],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent did you feel bad for your partner because of the outcome of the vote?')
    deserving = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, 'Slightly'],
        [3, ''],
        [4, 'Moderately'],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent did you partner deserve your help?')
    fairness = models.IntegerField(choices=C.StandardChoices,
                                   widget=widgets.RadioSelect,
                                   label='My helping behavior was influenced by a desire to be fair.')
    equality = models.IntegerField(choices=C.StandardChoices,
                                   widget=widgets.RadioSelect,
                                   label="My helping behavior was influenced by a desire to make my payoff and my partner's payoff more equal.")
    expectation_valence = models.StringField(
        choices=[
            ['Remote', mark_safe("<b>Fully remote policy:</b> Work remotely 5 full days per week.")],
            ['Hybrid', mark_safe("<b>Hybrid policy:</b> Work in-office 3 full days per week and remotely the remaining 2 full days.")],
            ['None', "I didn't consider which policy would win"]
        ],
        widget=widgets.RadioSelect,
    )
    expectation_strength = models.IntegerField(choices=C.StandardChoices,
                                               widget=widgets.RadioSelectHorizontal,
                                               blank=True)
    vote_valued = models.IntegerField(choices=C.StandardChoices,
                                          widget=widgets.RadioSelectHorizontal,
                                          label='The company values employee input on remote versus hybrid work policies.')

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
# 10. Help Completion Page
class a41(WaitPage):
    group_by_arrival_time = True
    title_text = 'Help Completion Page'
    body_text = 'The amount of help you have given to your partner has been recorded and both of your payoffs' \
                ' have been adjusted accordingly. You will automatically advance to the next page shortly where ' \
                'you will answer a few survey questions about the study…'

class a42(Page):
    form_model = 'player'
    form_fields = ['vote_preference', 'affect', 'identity_identify', 'identity_happy', 'identity_like', 'blame',
                   'sympathy', 'deserving', 'fairness', 'equality', 'expectation_valence', 'expectation_strength', 'vote_valued',]

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

page_sequence = [a41, a42]

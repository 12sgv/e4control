from otree.api import *
from otree.export import get_fields_for_csv
import random
import time

doc = """
App 2/6 in sequence.
App Before: instructions
App After: PEQ
---------------------------------------
Participants are grouped into groups upon arrival then vote on the firm policy
Then wait for group to finish vote before moving onto the next app
"""


class C(BaseConstants):
    NAME_IN_URL = 'c2'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = 5
    #PEQ Scales
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
        if len(waiting_players)>4:
            # put first 2 players in a pairing
            waiting_players[0].paired_group = self.session.vars['paired_group']
            waiting_players[1].paired_group = self.session.vars['paired_group']
            # increment the paired_group counter
            self.session.vars['paired_group'] += 1
            # put the second 2 players in a pairing
            waiting_players[2].paired_group = self.session.vars['paired_group']
            waiting_players[3].paired_group = self.session.vars['paired_group']
            # put the 5th player by themselves
            waiting_players[4].paired_group = 0
            waiting_players[4].not_paired = True
            waiting_players[4].paired_group = 0
            waiting_players[4].is_out = True
            # increment the group counter
            self.session.vars['paired_group'] += 1
            return waiting_players[:5]
        for player in waiting_players:
            if waiting_too_long_group_formation(player):
                player.group_formation_timeout = True
                player.participant.vars['group_formation_timeout'] = True
                player.is_out = True
                player.participant.vars['is_out'] = True
                return [player]

class Group(BaseGroup):
   pass

class Player(BasePlayer):
    #general vars
    is_out = models.BooleanField(initial=False)
    timed_out = models.BooleanField(initial=False)
    kicked_out = models.BooleanField(initial=False)
    #group pairing algorithm vars
    treatment = models.IntegerField()   #1: WW, 2:LL, 3:WL, 4:LW 5:5th Person
    paired_group = models.IntegerField()
    not_paired = models.BooleanField(initial=False)
    #page finished vars
    finished_voting = models.BooleanField(initial=False)
    finished_vote_outcome = models.BooleanField(initial=False)
    finished_giving = models.BooleanField(initial=False)
#    voted_remote = models.BooleanField()
    #page vars
    partner_check = models.IntegerField(
        widget=widgets.RadioSelect,
        doc="""Partner Manipulation Check""",
        label="Which of the following statements about you and your partner is true?",
        choices=[
            [1, 'We both voted the same and both won'],
            [2, 'We both voted the same and both lost'],
            [3, 'We voted different from one another, and my partner lost and I won'],
            [4, 'We voted different from one another, and my partner won and I lost'],
        ]
    )
    incorrect_count = models.IntegerField(initial=0)
    incorrect_answers = models.LongStringField(initial="")
    giving = models.IntegerField(
        doc="""Amount player helps their partner""",
        min=0,
        max=100,
        label="Amount of help I am giving to my partner:",
    )
    group_formation_timeout = models.BooleanField(initial=False)
    #PEQ Vars
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
                                               label="How confident were you that you would win the vote?",
                                               blank=True)



# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']


# PAGES
# 6. Team Advancement Page
class c21(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'You will automatically advance to the next page when' \
                ' all members of your team are ready to advance...'

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['group_formation_timeout'] == 1:
            return "c5"
        else:
            return None

    # timeout those who are waiting too long on this page and pay them the basic fee
    def before_next_page(self, timeout_happened):
        if timeout_happened:
            self.participant.vars['group_formation_timeout'] = 1
            self.participant.vars['earnings'] = self.session.config['participation_fee']
        else:
            self.participant.vars['group_formation_timeout'] = 0
            self.participant.vars['treatment'] = self.treatment



# this page is a buffer
class c22(Page):
    timeout_seconds = 0.001
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['not_paired'] = player.not_paired

#Additional Instructions Page
class c23(Page):
    # timeout set to session configs
    def get_timeout_seconds(self):
        return self.session.config['c_additional_instructions_timeout']

    # display for participants who have not timed out
    def is_displayed(player: Player):
        if player.group_formation_timeout == True:
            return False
        elif player.not_paired == True:
            return False
        else:
            return True

    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['paired_group'] = player.paired_group


#Helping (Main Group)
class c24(Page):
    #retrieve timeout seconds from the session configs
    def get_timeout_seconds(self):
        return self.session.config['offer_timeout']

    # only display if the participant is paired
    def is_displayed(player: Player):
        if player.not_paired == True:
            return False
        else:
            return True

    form_model = "player"
    form_fields = ["giving"]

    # custom error message if they did not select a number of points to give
    def error_message(player, values):
        if values['giving'] is None:
            return 'Please select the number of help points you want to give to your partner.'

    # give everything if the participant timed out
    def before_next_page(self, timeout_happened):
        # track when participant left this page to start timer for the next group formation page
        self.participant.vars['help_completion_time'] = time.time()
        self.participant.vars['giving'] = self.giving
        if timeout_happened:
            self.giving = 100
            self.participant.vars['payoff'] = 0
            self.participant.vars['giving'] = self.giving
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_help'] = True
            self.kicked_out = True
            self.participant.vars['kicked_out'] = True
            for p in self.group.get_players():
                if p.participant.vars['paired_group'] == self.participant.vars['paired_group'] and p.id_in_group != self.id_in_group:
                    p.participant.vars['other_timed_out'] = True
                    p.participant.vars['other_giving'] = 100
        else:
            self.finished_giving = True
            self.participant.vars['finished_giving'] = True

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'timed_out' in self.participant.vars and self.participant.vars['timed_out'] == 1:
            return "c5"
        else:
            return "c3"


#7b. Additional Instructions (5th Team Member who couldn't be paired)
class c25(Page):

    # display if the partner is not paired
    def is_displayed(player: Player):
        if player.not_paired:
            return True
        else:
            return False

    #pass on participant vars
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['not_paired'] = player.not_paired
        player.participant.vars['paired_group'] = player.paired_group
        player.participant.vars['is_out'] = player.is_out

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
            return "c4"


#######################################NOT USED###################################################################

#5th person short version alert page
class c26(Page):
    #Only show to the 5th person
    def is_displayed(player: Player):
        if player.not_paired == 1:
            return True
        else:
            return False


#Helping (5th Person)
class c27(Page):

    # only display if the participant is 5th participant
    def is_displayed(player: Player):
        if player.not_paired == 1:
            return True
        else:
            return False

    form_model = "player"
    form_fields = ["giving"]

    # custom error message if they did not select a number of points to give
    def error_message(player, values):
        if values['giving'] is None:
            return 'Please select the number of help points you would give your team member.'

    def vars_for_template(self):
        wonlost = "won" if self.winner == True else "lost"
        return {
            'wonlost': wonlost,
        }

    # give everything if the participant timed out
    def before_next_page(self, timeout_happened):
        # track when participant left this page to start timer for the next group formation page
        self.participant.vars['help_completion_time'] = time.time()
        self.participant.vars['giving'] = self.giving
        self.finished_giving = True
        self.participant.vars['finished_giving'] = True


#5th Person PEQ
class c28(Page):
    form_model = 'player'
    form_fields = ['vote_preference', 'vote_valued', 'affect', 'identity_identify', 'identity_happy', 'identity_like', 'blame',
                   'sympathy', 'expectation_valence', 'expectation_strength']

    def vars_for_template(self):
        return dict(
        #expectation_strength_label = "How confident were you that the fully {} policy would win?".format(self.participant.vars['policy_vote'])
        )

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['is_out'] == 1:
            return "c4"


page_sequence = [c21, c22, c23, c24, c25]
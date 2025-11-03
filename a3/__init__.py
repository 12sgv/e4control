from otree.api import *
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe
import random
import time

doc = """
MAIN TASK
App 3/5 in sequence.
App Before: a2 (Helping)
App After: a4 (PEQ)
---------------------------------------
Participants arrive here after all group members have helped.
Participants then Learn that their help is finalized.
Participants answer a helping PEQ.
Participants vote on a policy.
Participants answer a PEQ about the vote.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a3'
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
        'Somewhat',
        '',
        '',
        'A great extent',
    ]
    ConfidenceTable = [
        'Not at all confident',
        '',
        '',
        'Somewhat confident',
        '',
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
    EqualityTable = [
    'Only concerned about my cost',
    'Moderately more concerned about my cost',
    'Slightly more concerned about my cost',
    "Equally concerned about my cost & my partner's benefit",
    "Slightly more concerned about my partner's benefit",
    "Moderately more concerned about my partner's benefit",
    "Only concerned about my partner's benefit",
    ]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
   pass

class Player(BasePlayer):
    #timeout vars
    help_wait_timeout = models.BooleanField(initial=False)
    #page finished vars???
    finished_additional_instructions = models.BooleanField(initial=False)
    finished_help_completion = models.BooleanField(initial=False)
    #PEQ Helping Vars
    identity_identify = models.IntegerField(choices=C.StandardChoices,
                                            widget=widgets.RadioSelect,
                                            label='I identified with my partner.')
    identity_happy = models.IntegerField(choices=C.StandardChoices,
                                         widget=widgets.RadioSelect,
                                         label='I was happy to be paired with my partner.')
    identity_like = models.IntegerField(choices=C.StandardChoices,
                                        widget=widgets.RadioSelect,
                                        label='I liked my partner.')
    deserving = models.IntegerField(choices=[
        [0, 'Not at all'],
        [1, ''],
        [2, 'Slightly'],
        [3, ''],
        [4, 'Moderately'],
        [5, ''],
        [6, 'A great extent']],
        widget=widgets.RadioSelect,
        label='To what extent did your partner deserve your help?')
    fair_help = models.IntegerField(choices=C.StandardChoices,
                                    widget=widgets.RadioSelect,
                                    label='It was fair for my partner to ask for my help.')
    equality = models.IntegerField(choices=[
        [-3, 'Only concerned about my cost'],
        [-2, 'Moderately more concerned about my cost'],
        [-1, 'Slightly more concerned about my cost'],
        [0, "Equally concerned about my cost and my partner's benefit"],
        [1, "Slightly more concerned about my partner's benefit"],
        [2, "Moderately more concerned about my partner's benefit"],
        [3, "Only concerned about my partner's benefit"]],
        widget=widgets.RadioSelect,
        label='When deciding how much to help your partner, were you more concerned about the cost to you or the benefit to your partner?')
    #PEQ Voting Vars
    policy_vote = models.StringField(
        choices=[
            ['Remote', mark_safe("<b>Fully remote policy:</b> Work remotely 5 full days per week.")],
            ['Hybrid', mark_safe("<b>Hybrid policy:</b> Work in-office 3 full days per week and remotely the remaining 2 full days.")]
        ],
        label=mark_safe("<b>I would vote for the:</b>"),
        widget=widgets.RadioSelect
    )
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
    other_helping = models.IntegerField()


# PAGES
# 8. Help Completion Page
class a31(WaitPage):
#    wait_for_all_groups = False
    title_text = 'Help Completion Page'
    body_text = ('The amount of help you have given to your partner has been recorded and both of your bonus amounts '
                 'have been adjusted accordingly. You will automatically advance to the next page shortly where you will'
                 ' answer a few survey questions about the study...')

    # dynamically set timeout from session var
    def get_timeout_seconds(self):
        return self.session.vars.get('help_wait_timeout')  # None = no timeout if not set

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant.vars['help_wait_timeout'] = 1


# this page is a buffer
class a32(Page):
    timeout_seconds = 0.001

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print("Start setting other helping on buffer 32 for participant with group id", player.id_in_group)

            group_size = len(player.group.get_players())
            partner_id = player.id_in_group - 1 if player.id_in_group > 1 else group_size
            partner = player.group.get_player_by_id(partner_id)
            #Copy partner's helping
            player.other_helping = partner.participant.vars['helping']
            player.participant.vars['other_helping'] = player.other_helping

            #Check if partner timed out on help page
            if partner.participant.vars.get('timed_out_help'):
                player.participant.vars['other_timed_out'] = True
            else:
                player.participant.vars['other_timed_out'] = False

            print("End setting other helping on buffer 32", player.id_in_group, "->", player.other_helping)


#Help Completion Page
class a33(Page):
    # display for participants who have not timed out
    def is_displayed(player: Player):
        if player.participant.vars['is_out'] == True:
            return False
        else:
            return True

    def before_next_page(self, timeout_happened):
        self.finished_help_completion = True


#Survey (Help Questions)
class a34(Page):
    # only display if the participant is not out
    def is_displayed(player: Player):
        if player.participant.vars['is_out'] == True:
            return False
        else:
            return True

    form_model = "player"
    form_fields = ['identity_identify', 'identity_happy', 'identity_like', 'deserving','equality',]


#Survey (Help Questions)
class a34(Page):
    # only display if the participant is not out
    def is_displayed(player: Player):
        if player.participant.vars['is_out'] == True:
            return False
        else:
            return True

    form_model = "player"
    form_fields = ['identity_identify', 'identity_happy', 'identity_like', 'deserving', 'fair_help', 'equality',]

    def before_next_page(player, timeout_happened):
        player.participant.vars['identity_identify'] = player.identity_identify
        player.participant.vars['identity_happy'] = player.identity_happy
        player.participant.vars['identity_like'] = player.identity_like
        player.participant.vars['deserving'] = player.deserving
        player.participant.vars['fair_help'] = player.fair_help
        player.participant.vars['equality'] = player.equality

#5. Voting
class a35(Page):
    # only display if the participant is not out
    def is_displayed(player: Player):
        if player.participant.vars['is_out'] == True:
            return False
        else:
            return True

    form_model = 'player'
    form_fields = ['policy_vote']

    def before_next_page(self, timeout_happened):
        self.participant.vars['policy_vote'] = self.policy_vote

#Survey (Vote Questions)
class a36(Page):
    # only display if the participant is not out
    def is_displayed(player: Player):
        if player.participant.vars['is_out'] == True:
            return False
        else:
            return True

    form_model = "player"
    form_fields = ['vote_preference', 'expectation_valence', 'expectation_strength']


page_sequence = [a31, a32, a33, a34, a35, a36]
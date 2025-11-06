from otree.api import *
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe
import random
import time

doc = """
MAIN TASK
App 2/4 in sequence.
App Before: a1 (Instructions)
App After: a4 (PEQ)
---------------------------------------
Participants arrive after introduction.
Participants begin the app by waiting for their team of 5 to arrive.
They then complete the main experimental helping task with their team.
All participants in the main group advance to the vote portion (a3) after this app.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a2'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = 5
    # PEQ Scales
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
    def group_by_arrival_time_method(self, waiting_players):
        wait_list = [p for p in waiting_players]
        #timeout if waiting too long
        for player in waiting_players:
            if waiting_too_long_group_formation(player):
                player.group_formation_timeout = True
                player.participant.vars['group_formation_timeout'] = True
                player.group_formation_timeout = True
                player.is_out = True
                player.participant.vars['is_out'] = True
                return [player]
        #wait until at least 5 are waiting and then advance them with the proper vars
        if len(wait_list) >= 5:
            #assign group number var
            wait_list[0].participant.vars['group_number'] = self.session.vars['group_number']
            wait_list[1].participant.vars['group_number'] = self.session.vars['group_number']
            wait_list[2].participant.vars['group_number'] = self.session.vars['group_number']
            wait_list[3].participant.vars['group_number'] = self.session.vars['group_number']
            wait_list[4].participant.vars['group_number'] = self.session.vars['group_number']
            #increment session group number
            self.session.vars['group_number'] += 1
            # advance group
            return wait_list[:5]
        #keep people in waiting room
        else:
            return None

class Group(BaseGroup):
   pass

class Player(BasePlayer):
    policy_vote = models.StringField(
        choices=[
            ['Remote', mark_safe("<b>Fully remote policy:</b> Work remotely 5 full days per week.")],
            ['Hybrid', mark_safe("<b>Hybrid policy:</b> Work in-office 3 full days per week and remotely the remaining 2 full days.")]
        ],
        label=mark_safe("<b>I vote for the:</b>"),
        widget=widgets.RadioSelect
    )
    #timeout vars
    is_out = models.BooleanField(initial=False)
    timed_out = models.BooleanField(initial=False)
    kicked_out = models.BooleanField(initial=False)
    group_formation_timeout = models.BooleanField(initial=False)
    #group pairing algorithm vars
    group_number = models.IntegerField()
    other_player = models.IntegerField()
    #page finished vars
    finished_additional_instructions = models.BooleanField(initial=False)
    finished_helping = models.BooleanField(initial=False)
    #page vars
    helping = models.IntegerField(
        doc="""Amount player helps their partner""",
        label="Amount of help I am giving to my partner:",
        blank=False,
        choices=[
            0,5,10,15,20,25,30,35,40,45,50,55,60,
        ],
    )
    ### a3 Vars
    # timeout vars
    help_wait_timeout = models.BooleanField(initial=False)
    # page finished vars???
    finished_additional_instructions = models.BooleanField(initial=False)
    finished_help_completion = models.BooleanField(initial=False)
    # PEQ Helping Vars
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
    # PEQ Voting Vars
    policy_vote = models.StringField(
        choices=[
            ['Remote', mark_safe("<b>Fully remote policy:</b> Work remotely 5 full days per week.")],
            ['Hybrid', mark_safe(
                "<b>Hybrid policy:</b> Work in-office 3 full days per week and remotely the remaining 2 full days.")]
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
            ['Hybrid', mark_safe(
                "<b>Hybrid policy:</b> Work in-office 3 full days per week and remotely the remaining 2 full days.")],
            ['None', "I didn't consider which policy I expected to win"]
        ],
        widget=widgets.RadioSelect,
    )
    expectation_strength = models.IntegerField(choices=C.StandardChoices,
                                               widget=widgets.RadioSelectHorizontal,
                                               blank=True)
    other_helping = models.IntegerField()

# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']

# PAGES
# 6a. Team Advancement Page (Main Group)
class a21(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'You will automatically advance to the next page when your team is formed...'

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['group_formation_timeout'] == True:
            return "a5"
        else:
            return None

# this page is a buffer
class a22(Page):
    timeout_seconds = 0.001
    def before_next_page(player: Player, timeout_happened):
        player.group_number = player.participant.vars['group_number']
        player.participant.vars['help_arrival'] = time.time()


#Additional Instructions
class a23(Page):
    # timeout set to session configs
    def get_timeout_seconds(self):
        return self.session.config['additional_instructions_timeout']

    # display for participants who have not timed out
    def is_displayed(player: Player):
        if player.group_formation_timeout == True or player.is_out == True:
            return False
        else:
            return True

    def before_next_page(self, timeout_happened):
        self.finished_additional_instructions = True


#Helping (Main Group)
class a24(Page):
    #retrieve timeout seconds from the session configs
    def get_timeout_seconds(self):
        return self.session.config['offer_timeout']

    # only display if the participant is not out
    def is_displayed(player: Player):
        if player.is_out == True:
            return False
        else:
            return True

    form_model = "player"
    form_fields = ["helping"]

    # custom error message if they did not select a number of points to give
    def error_message(player, values):
        if values['helping'] is None:
            return 'Please select the number of help points you want to give to your partner.'

    # give everything if the participant timed out
    def before_next_page(self, timeout_happened):
        # track when participant left this page to start timer for the next group formation page
        self.participant.vars['help_completion_time'] = time.time()
        self.participant.vars['helping'] = self.helping
        if timeout_happened:
            self.helping = 60
            self.participant.vars['payoff'] = 0
            self.participant.vars['earnings'] = 0
            self.participant.vars['helping'] = self.helping
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_help'] = True
            self.kicked_out = True
            self.participant.vars['kicked_out'] = True
        else:
            self.finished_helping = True
            self.participant.vars['finished_helping'] = True

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'timed_out' in self.participant.vars and self.participant.vars['timed_out'] == 1:
            return "a5"


class a31(WaitPage):
    wait_for_all_groups = False
    title_text = 'Help Completion Page'
    body_text = ('The amount of help you have given to your partner has been recorded and both of your bonus amounts '
                 'have been adjusted accordingly. You will automatically advance to the next page shortly where you will'
                 ' answer a few survey questions about the study...')

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

page_sequence = [a21, a22, a23, a24, a31, a32, a33, a34, a35, a36]
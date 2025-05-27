from otree.api import *
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe
import random
import time

doc = """
MAIN TASK
App 2/6 in sequence.
App Before: a1 (Instructions)
App After: a4 (PEQ)
---------------------------------------
Participants in the main group arrive here after voting in a1.
Participants begin the app by waiting for their team of 5 to arrive.
Four of the participants are part of the main group and are paired with one other member of the main group.
They then complete the main experimental task with their partners.
The fifth participant in the main group is not paired with another team member.
This fifth participant completes a hypothetical version of the main task.
All participants in the main group advance to the PEQ (a4) after this app.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a2'
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

class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        #Set this as a session var
        hybrid_votes = [p for p in waiting_players if p.participant.vars['policy_vote'] == 'Hybrid']
        remote_votes = [p for p in waiting_players if p.participant.vars['policy_vote'] == 'Remote']
        #group_type 1 is same pairing with remote winning
        if self.session.vars['group_type'] == 1:
            #Make it so remote wins 3-2
            if len(hybrid_votes) >= 2 and len(remote_votes) >= 3:
                #Assign group type to the participants
                hybrid_votes[0].group_type = self.session.vars['group_type']
                hybrid_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                remote_votes[2].group_type = self.session.vars['group_type']
                #increment group_type session variable
                self.session.vars['group_type'] = 2
                #Set alignment variable
                hybrid_votes[0].aligned = True
                hybrid_votes[1].aligned = True
                remote_votes[0].aligned = True
                remote_votes[1].aligned = True
                #Set winning policy
                hybrid_votes[0].remote_won = True
                hybrid_votes[1].remote_won = True
                remote_votes[0].remote_won = True
                remote_votes[1].remote_won = True
                remote_votes[2].remote_won = True
                #Set outcome variable
                hybrid_votes[0].winner = False
                hybrid_votes[1].winner = False
                remote_votes[0].winner = True
                remote_votes[1].winner = True
                remote_votes[2].winner = True
                #Assign variable to track treatment
                hybrid_votes[0].treatment = 2
                hybrid_votes[1].treatment = 2
                remote_votes[0].treatment = 1
                remote_votes[1].treatment = 1
                remote_votes[2].treatment = 5
                #assign participants to the group number and increment group for each group
                hybrid_votes[0].group_number = self.session.vars['group_number']
                hybrid_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[0].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[2].group_number = 0
                #assign partner id variable
                hybrid_votes[0].participant.vars['partner_id'] = hybrid_votes[1].id_in_subsession
                hybrid_votes[1].participant.vars['partner_id'] = hybrid_votes[0].id_in_subsession
                remote_votes[0].participant.vars['partner_id'] = remote_votes[1].id_in_subsession
                remote_votes[1].participant.vars['partner_id'] = remote_votes[0].id_in_subsession
                #assign vars to fifth person
                remote_votes[2].is_out = True
                remote_votes[2].participant.vars['is_out'] = True
                remote_votes[2].not_paired = True
                remote_votes[2].participant.vars['not_paired'] = True
                # advance group
                return hybrid_votes[:2] + remote_votes[:3]
        #group_type 2 is same pairing with hybrid winning
        elif self.session.vars['group_type'] == 2:
            if len(hybrid_votes) >=3 and len(remote_votes) >= 2:
                hybrid_votes[0].group_type = self.session.vars['group_type']
                hybrid_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                hybrid_votes[2].group_type = self.session.vars['group_type']
                # increment group_type session variable
                self.session.vars['group_type'] = 3
                # Set alignment variable
                hybrid_votes[0].aligned = True
                hybrid_votes[1].aligned = True
                remote_votes[0].aligned = True
                remote_votes[1].aligned = True
                # Set winning policy
                hybrid_votes[0].remote_won = False
                hybrid_votes[1].remote_won = False
                hybrid_votes[2].remote_won = False
                remote_votes[0].remote_won = False
                remote_votes[1].remote_won = False
                # Set outcome variable
                hybrid_votes[0].winner = True
                hybrid_votes[1].winner = True
                hybrid_votes[2].winner = True
                remote_votes[0].winner = False
                remote_votes[1].winner = False
                # Assign variable to track treatment
                hybrid_votes[0].treatment = 1
                hybrid_votes[1].treatment = 1
                hybrid_votes[2].treatment = 5
                remote_votes[0].treatment = 2
                remote_votes[1].treatment = 2
                # assign participants to the group number and increment group for each group
                hybrid_votes[0].group_number = self.session.vars['group_number']
                hybrid_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[0].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                hybrid_votes[2].group_number = 0
                # assign partner id variable
                hybrid_votes[0].participant.vars['partner_id'] = hybrid_votes[1].id_in_subsession
                hybrid_votes[1].participant.vars['partner_id'] = hybrid_votes[0].id_in_subsession
                remote_votes[0].participant.vars['partner_id'] = remote_votes[1].id_in_subsession
                remote_votes[1].participant.vars['partner_id'] = remote_votes[0].id_in_subsession
                # assign vars to fifth person
                hybrid_votes[2].is_out = True
                hybrid_votes[2].participant.vars['is_out'] = True
                hybrid_votes[2].not_paired = True
                hybrid_votes[2].participant.vars['not_paired'] = True
                # advance group
                return hybrid_votes[:3] + remote_votes[:2]
        #group_type 3 is different pairing with remote winning
        elif self.session.vars['group_type'] == 3:
            if len(hybrid_votes) >= 2 and len(remote_votes) >= 3:
                hybrid_votes[0].group_type = self.session.vars['group_type']
                hybrid_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                remote_votes[2].group_type = self.session.vars['group_type']
                # Increment group_type session variable
                self.session.vars['group_type'] = 4
                # Set alignment variable
                hybrid_votes[0].aligned = False
                hybrid_votes[1].aligned = False
                remote_votes[0].aligned = False
                remote_votes[1].aligned = False
                # Set winning policy
                hybrid_votes[0].remote_won = True
                hybrid_votes[1].remote_won = True
                remote_votes[0].remote_won = True
                remote_votes[1].remote_won = True
                remote_votes[2].remote_won = True
                # Set outcome variable
                hybrid_votes[0].winner = False
                hybrid_votes[1].winner = False
                remote_votes[0].winner = True
                remote_votes[1].winner = True
                remote_votes[2].winner = True
                # Assign variable to track treatment
                hybrid_votes[0].treatment = 4
                hybrid_votes[1].treatment = 4
                remote_votes[0].treatment = 3
                remote_votes[1].treatment = 3
                remote_votes[2].treatment = 5
                # assign participants to the group number and increment group for each group
                hybrid_votes[0].group_number = self.session.vars['group_number']
                remote_votes[0].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                hybrid_votes[1].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[2].group_number = 0
                # assign partner id variable
                hybrid_votes[0].participant.vars['partner_id'] = remote_votes[0].id_in_subsession
                remote_votes[0].participant.vars['partner_id'] = hybrid_votes[0].id_in_subsession
                hybrid_votes[1].participant.vars['partner_id'] = remote_votes[1].id_in_subsession
                remote_votes[1].participant.vars['partner_id'] = hybrid_votes[1].id_in_subsession
                # assign vars to fifth person
                remote_votes[2].is_out = True
                remote_votes[2].participant.vars['is_out'] = True
                remote_votes[2].not_paired = True
                remote_votes[2].participant.vars['not_paired'] = True
                # advance group
                return hybrid_votes[:2] + remote_votes[:3]
        #group type 4 is different pairing with hybrid winning
        elif self.session.vars['group_type'] == 4:
            if len(hybrid_votes) >= 3 and len(remote_votes) >= 2:
                hybrid_votes[0].group_type = self.session.vars['group_type']
                hybrid_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                hybrid_votes[2].group_type = self.session.vars['group_type']
                # Increment group_type session variable
                self.session.vars['group_type'] = 1
                # Set alignment variable
                hybrid_votes[0].aligned = False
                hybrid_votes[1].aligned = False
                remote_votes[0].aligned = False
                remote_votes[1].aligned = False
                # Set winning policy
                hybrid_votes[0].remote_won = False
                hybrid_votes[1].remote_won = False
                hybrid_votes[2].remote_won = False
                remote_votes[0].remote_won = False
                remote_votes[1].remote_won = False
                # Set outcome variable
                hybrid_votes[0].winner = True
                hybrid_votes[1].winner = True
                hybrid_votes[2].winner = True
                remote_votes[0].winner = False
                remote_votes[1].winner = False
                # Assign variable to track treatment
                hybrid_votes[0].treatment = 3
                hybrid_votes[1].treatment = 3
                hybrid_votes[2].treatment = 5
                remote_votes[0].treatment = 4
                remote_votes[1].treatment = 4
                # assign participants to the group number and increment group for each group
                hybrid_votes[0].group_number = self.session.vars['group_number']
                remote_votes[0].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                hybrid_votes[1].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                hybrid_votes[2].group_number = 0
                # assign partner id variable
                hybrid_votes[0].participant.vars['partner_id'] = remote_votes[0].id_in_subsession
                remote_votes[0].participant.vars['partner_id'] = hybrid_votes[0].id_in_subsession
                hybrid_votes[1].participant.vars['partner_id'] = remote_votes[1].id_in_subsession
                remote_votes[1].participant.vars['partner_id'] = hybrid_votes[1].id_in_subsession
                # assign vars to fifth person
                hybrid_votes[2].is_out = True
                hybrid_votes[2].participant.vars['is_out'] = True
                hybrid_votes[2].not_paired = True
                hybrid_votes[2].participant.vars['not_paired'] = True
                # advance group
                return hybrid_votes[:3] + remote_votes[:2]
        else:
            return None

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
    group_type = models.IntegerField()
    aligned = models.BooleanField()
    remote_won = models.BooleanField()
    winner = models.BooleanField()
    treatment = models.IntegerField()   #1: WW, 2:LL, 3:WL, 4:LW 5:5th Person
    group_number = models.IntegerField()
    not_paired = models.BooleanField()
    other_player = models.IntegerField()
    #page finished vars
    finished_voting = models.BooleanField(initial=False)
    finished_vote_outcome = models.BooleanField(initial=False)
    finished_helping = models.BooleanField(initial=False)
#    voted_remote = models.BooleanField()
    #page vars
    partner_check = models.IntegerField(
        widget=widgets.RadioSelect,
        doc="""Partner Manipulation Check""",
        label="Which of the following statements about you and your partner is true?",
        choices=[
            [1, 'We both voted the same and both won'],
            [2, 'We both voted the same and both lost'],
            [3, 'We voted different from one another, and I won and my partner lost'],
            [4, 'We voted different from one another, and I lost and my partner won'],
        ]
    )
    incorrect_count = models.IntegerField(initial=0)
    incorrect_answers = models.LongStringField(initial="")
    helping = models.IntegerField(
        doc="""Amount player helps their partner""",
        label="Amount of help I am giving to my partner:",
        blank=False,
        choices=[
            0,5,10,15,20,25,30,35,40,45,50,55,60,
        ],
    )
    group_formation_timeout = models.BooleanField(initial=False)
    #PEQ Vars
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
    fairness = models.IntegerField(choices=C.StandardChoices,
                                   widget=widgets.RadioSelect,
                                   label='My helping behavior was influenced by a desire to be fair.')
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

# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']

# retrieve what other player provided
def other_helping(self):
    if self.id_in_group == 1:
        other_player = self.group.get_player_by_id(2)
        self.participant.vars['partner__id'] = other_player.participant.id_in_session
    elif self.id_in_group == 2:
        other_player = self.group.get_player_by_id(1)
        self.participant.vars['partner_id'] = other_player.participant.id_in_session
    else:
        print("no id in group for this player. Player group id:", self.id_in_group)
    self.participant.vars['other_helping'] = other_player.helping
    return self.participant.vars['other_helping']


# PAGES
# 6a. Team Advancement Page (Main Group)
class a21(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'Your vote has been recorded. You will automatically advance to the next page when' \
                ' all members of your team are ready to advance...'

    def after_all_players_arrive(self):
        group = self.group
        # retrieve group_id
        for player in group.get_players():
            if not player.is_out:
                player.participant.vars['vote_group_id'] = group.id_in_subsession
                player.participant.vars['group_type'] = player.group_type
                player.participant.vars['aligned'] = player.aligned
                player.participant.vars['remote_won'] = player.remote_won
                player.participant.vars['winner'] = player.winner
                player.participant.vars['treatment'] = player.treatment
                player.participant.vars['group_number'] = player.group_number
            else:
                player.participant.vars['winner'] = player.field_maybe_none('winner')


    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['group_formation_timeout'] == 1:
            return "a6"
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
class a22(Page):
    timeout_seconds = 0.001
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['group_number'] = player.group_number

#Vote Result
class a23(Page):
    # timeout set to session configs
    def get_timeout_seconds(self):
        return self.session.config['vote_outcome_timeout']

    # display for participants who have not timed out
    def is_displayed(player: Player):
        if player.group_formation_timeout == True or player.is_out == True:
            return False
        else:
            return True

    def vars_for_template(self):
        outcome = "fully remote" if self.remote_won == True else "hybrid"
        vote = "fully remote" if self.participant.vars['policy_vote'] == "Remote" else "hybrid"
        outcome_effect = self.session.config['outcome_payoff_effect']
        return {
            'outcome': outcome,
            'vote': vote,
            'outcome_effect': outcome_effect,
        }

    def before_next_page(self, timeout_happened):
        self.finished_vote_outcome = True
        self.participant.vars['treatment'] = self.treatment


#Partner Check
class a24(Page):
    # retrieve the timeout seconds for this page from the session configs
    def get_timeout_seconds(self):
        return self.session.config['partner_check_timeout']

    # display if the partner is not out
    def is_displayed(player: Player):
        if player.is_out:
            return False
        else:
            return True

    form_model = 'player'
    form_fields = ['partner_check']

    # custom error message if they answered incorrectly
    def error_message(player, value):
        if value['partner_check'] != player.treatment:
            player.incorrect_count += 1
            player.incorrect_answers += str(value)[-2]
            return 'You answered incorrectly. Please read the information on the page again to make sure you ' \
                   'understand the outcome of the vote and whether you and your partner won or lost the vote.'

    def vars_for_template(self):
        outcome = "fully remote" if self.remote_won == True else "hybrid"
        vote = "fully remote" if self.participant.vars['policy_vote'] == "Remote" else "hybrid"
        othervote = "hybrid" if self.treatment == 3 and self.remote_won == True else "fully remote"
        outcome_effect = self.session.config['outcome_payoff_effect']
        return {
            'vote': vote,
            'outcome': outcome,
            'othervote': othervote,
            'outcome_effect': outcome_effect,
        }

    def before_next_page(self, timeout_happened):
        # timeout means that they give everything to their partner
        if timeout_happened:
            self.helping = 100
            self.participant.vars['helping'] = 100
            self.timed_out = True
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_partner_check'] = True
            self.kicked_out = True
            self.participant.vars['kicked_out'] = True
            for p in self.group.get_players():
                if p.participant.vars['group_number'] == self.participant.vars['group_number'] and p.id_in_group != self.id_in_group:
                    p.participant.vars['other_timed_out'] = True
                    p.participant.vars['other_helping'] = 100



    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'timed_out' in self.participant.vars and self.participant.vars['timed_out'] == 1:
            return "a6"

#Helping (Main Group)
class a25(Page):
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

    def vars_for_template(self):
        vote = "fully remote" if self.participant.vars['policy_vote'] == "Remote" else "hybrid"
        othervote = "hybrid" if self.treatment == 3 and self.remote_won == True else "fully remote"
        return {
            'vote': vote,
            'othervote': othervote,
        }

    # give everything if the participant timed out
    def before_next_page(self, timeout_happened):
        # track when participant left this page to start timer for the next group formation page
        self.participant.vars['help_completion_time'] = time.time()
        self.participant.vars['helping'] = self.helping
        self.participant.vars['group_number'] = self.group_number
        if timeout_happened:
            self.helping = 100
            self.participant.vars['payoff'] = 0
            self.participant.vars['helping'] = self.helping
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_help'] = True
            self.kicked_out = True
            self.participant.vars['kicked_out'] = True
            for p in self.group.get_players():
                if p.participant.vars['group_number'] == self.participant.vars['group_number'] and p.id_in_group != self.id_in_group:
                    p.participant.vars['other_timed_out'] = True
                    p.participant.vars['other_helping'] = 100
        else:
            self.finished_helping = True
            self.participant.vars['finished_helping'] = True

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'timed_out' in self.participant.vars and self.participant.vars['timed_out'] == 1:
            return "a6"
        else:
            return "a4"


###### 5th Person Info #######

#5th person short version alert page
class a26(Page):
    #Only show to the 5th person
    def is_displayed(player: Player):
        if player.participant.vars['not_paired'] == 1:
            return True
        else:
            return False

    def app_after_this_page(self, upcoming_apps):
        return "a6"


page_sequence = [a21, a22, a23, a24, a25, a26]
from otree.api import *
from otree.export import get_fields_for_csv
from django.utils.safestring import mark_safe
import random
import time

doc = """
MAIN TASK
App 2/5 in sequence.
App Before: a1 (Instructions)
App After: a3 (Voting)
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

# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']

# PAGES
# 6a. Team Advancement Page (Main Group)
class a21(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'You will automatically advance to the next page when all members of your team are ready to advance...'

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
        else:
            return "a3"

page_sequence = [a21, a22, a23, a24]
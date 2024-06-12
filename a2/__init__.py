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
    NAME_IN_URL = 'a2'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = 5


class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        #Set this as a session var
        office_votes = [p for p in waiting_players if p.participant.vars['policy_vote'] == 'Office']
        remote_votes = [p for p in waiting_players if p.participant.vars['policy_vote'] == 'Remote']
        #group_type 1 is same pairing with remote winning
        if self.session.vars['group_type'] == 1:
            #Make it so remote wins 3-2
            if len(office_votes) >= 2 and len(remote_votes) >= 3:
                #Assign group type to the participants
                office_votes[0].group_type = self.session.vars['group_type']
                office_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                remote_votes[2].group_type = self.session.vars['group_type']
                #increment group_type session variable
                self.session.vars['group_type'] = 2
                #Set alignment variable
                office_votes[0].aligned = True
                office_votes[1].aligned = True
                remote_votes[0].aligned = True
                remote_votes[1].aligned = True
                #Set winning policy
                office_votes[0].remote_won = True
                office_votes[1].remote_won = True
                remote_votes[0].remote_won = True
                remote_votes[1].remote_won = True
                #Set outcome variable
                office_votes[0].winner = False
                office_votes[1].winner = False
                remote_votes[0].winner = True
                remote_votes[1].winner = True
                #Assign variable to track treatment
                office_votes[0].treatment = 2
                office_votes[1].treatment = 2
                remote_votes[0].treatment = 1
                remote_votes[1].treatment = 1
                #assign participants to the group number and increment group for each group
                office_votes[0].group_number = self.session.vars['group_number']
                office_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[0].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                #assign vars to fifth person
                remote_votes[2].is_out = True
                remote_votes[2].participant.vars['is_out'] = True
                remote_votes[2].not_paired = True
                remote_votes[2].participant.vars['not_paired'] = True
                # advance group
                return office_votes[:2] + remote_votes[:3]
        #group_type 2 is same pairing with office winning
        elif self.session.vars['group_type'] == 2:
            if len(office_votes) >=3 and len(remote_votes) >= 2:
                office_votes[0].group_type = self.session.vars['group_type']
                office_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                office_votes[2].group_type = self.session.vars['group_type']
                # increment group_type session variable
                self.session.vars['group_type'] = 3
                # Set alignment variable
                office_votes[0].aligned = True
                office_votes[1].aligned = True
                remote_votes[0].aligned = True
                remote_votes[1].aligned = True
                # Set winning policy
                office_votes[0].remote_won = False
                office_votes[1].remote_won = False
                remote_votes[0].remote_won = False
                remote_votes[1].remote_won = False
                # Set outcome variable
                office_votes[0].winner = True
                office_votes[1].winner = True
                remote_votes[0].winner = False
                remote_votes[1].winner = False
                # Assign variable to track treatment
                office_votes[0].treatment = 1
                office_votes[1].treatment = 1
                remote_votes[0].treatment = 2
                remote_votes[1].treatment = 2
                # assign participants to the group number and increment group for each group
                office_votes[0].group_number = self.session.vars['group_number']
                office_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                remote_votes[0].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                # assign vars to fifth person
                office_votes[2].is_out = True
                office_votes[2].participant.vars['is_out'] = True
                office_votes[2].not_paired = True
                office_votes[2].participant.vars['not_paired'] = True
                # advance group
                return office_votes[:3] + remote_votes[:2]
        #group_type 3 is different pairing with remote winning
        elif self.session.vars['group_type'] == 3:
            if len(office_votes) >= 2 and len(remote_votes) >= 3:
                office_votes[0].group_type = self.session.vars['group_type']
                office_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                remote_votes[2].group_type = self.session.vars['group_type']
                # Increment group_type session variable
                self.session.vars['group_type'] = 4
                # Set alignment variable
                office_votes[0].aligned = False
                office_votes[1].aligned = False
                remote_votes[0].aligned = False
                remote_votes[1].aligned = False
                # Set winning policy
                office_votes[0].remote_won = True
                office_votes[1].remote_won = True
                remote_votes[0].remote_won = True
                remote_votes[1].remote_won = True
                # Set outcome variable
                office_votes[0].winner = False
                office_votes[1].winner = False
                remote_votes[0].winner = True
                remote_votes[1].winner = True
                # Assign variable to track treatment
                office_votes[0].treatment = 4
                office_votes[1].treatment = 4
                remote_votes[0].treatment = 3
                remote_votes[1].treatment = 3
                # assign participants to the group number and increment group for each group
                office_votes[0].group_number = self.session.vars['group_number']
                remote_votes[0].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                office_votes[1].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                # assign vars to fifth person
                remote_votes[2].is_out = True
                remote_votes[2].participant.vars['is_out'] = True
                remote_votes[2].not_paired = True
                remote_votes[2].participant.vars['not_paired'] = True
                # advance group
                return office_votes[:2] + remote_votes[:3]
        #group type 4 is different pairing with office winning
        elif self.session.vars['group_type'] == 4:
            if len(office_votes) >= 3 and len(remote_votes) >= 2:
                office_votes[0].group_type = self.session.vars['group_type']
                office_votes[1].group_type = self.session.vars['group_type']
                remote_votes[0].group_type = self.session.vars['group_type']
                remote_votes[1].group_type = self.session.vars['group_type']
                office_votes[2].group_type = self.session.vars['group_type']
                # Increment group_type session variable
                self.session.vars['group_type'] = 1
                # Set alignment variable
                office_votes[0].aligned = False
                office_votes[1].aligned = False
                remote_votes[0].aligned = False
                remote_votes[1].aligned = False
                # Set winning policy
                office_votes[0].remote_won = False
                office_votes[1].remote_won = False
                remote_votes[0].remote_won = False
                remote_votes[1].remote_won = False
                # Set outcome variable
                office_votes[0].winner = True
                office_votes[1].winner = True
                remote_votes[0].winner = False
                remote_votes[1].winner = False
                # Assign variable to track treatment
                office_votes[0].treatment = 3
                office_votes[1].treatment = 3
                remote_votes[0].treatment = 4
                remote_votes[1].treatment = 4
                # assign participants to the group number and increment group for each group
                office_votes[0].group_number = self.session.vars['group_number']
                remote_votes[0].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                office_votes[1].group_number = self.session.vars['group_number']
                remote_votes[1].group_number = self.session.vars['group_number']
                self.session.vars['group_number'] += 1
                # assign vars to fifth person
                office_votes[2].is_out = True
                office_votes[2].participant.vars['is_out'] = True
                office_votes[2].not_paired = True
                office_votes[2].participant.vars['not_paired'] = True
                # advance group
                return office_votes[:3] + remote_votes[:2]
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
    #group pairing algorithm vars
    group_type = models.IntegerField()
    aligned = models.BooleanField()
    remote_won = models.BooleanField()
    winner = models.BooleanField()
    treatment = models.IntegerField()   #1: WW, 2:LL, 3:WL, 4:LW
    group_number = models.IntegerField()
    not_paired = models.BooleanField()
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



# function to see if the player should time out on the first wait page (groupassignment waitpage)
def waiting_too_long_group_formation(self):
    return time.time() - self.participant.vars['group_formation_arrival'] > self.session.config[
        'group_formation_timeout']


# PAGES
class GroupAssignment(WaitPage):
    group_by_arrival_time = True
    title_text = 'Team Advancement Page'
    body_text = 'Your vote has been recorded. You will automatically advance to the next page when' \
                ' all members of your team are ready to advance...'

    def after_all_players_arrive(self):
        group = self.group
        # retrieve group_id
        for player in group.get_players():
            player.participant.vars['vote_group_id'] = group.id_in_subsession

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['group_formation_timeout'] == 1:
            return "payment_info"
        else:
            return None

    # timeout those who are waiting too long on this page and pay them the basic fee
    def before_next_page(self, timeout_happened):
        if timeout_happened:
            self.participant.vars['group_formation_timeout'] = 1
            self.participant.vars['calculated_payoff'] = int(2.50)
        else:
            self.participant.vars['group_formation_timeout'] = 0
            self.participant.vars['treatment'] = self.treatment


# this page is a buffer
class NoGroup(Page):
    timeout_seconds = 0.001

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['is_out'] == 1:
            return "survey"

class VoteOutcome(Page):
    # timeout set to session configs
    def get_timeout_seconds(self):
        return self.session.config['vote_outcome_timeout']

    # display for participants who have not timed out
    def is_displayed(player: Player):
        if player.is_out == True:
            return False
        else:
            return True

    def vars_for_template(self):
        outcome = "remote" if self.remote_won == True else "office"
        vote = "remote" if self.participant.vars['policy_vote'] == "Remote" else "office"
        wonlost = "won" if self.winner == True else "lost"
        return {
            'outcome': outcome,
            'vote': vote,
            'wonlost': wonlost,
        }

    def before_next_page(self, timeout_happened):
        self.finished_vote_outcome = True
        self.participant.vars['treatment'] = self.treatment
#        added_pairings = self.session.vars.get('added_pairings', [])  # Set to keep track of already added pairings
#        # retrieve partner informaiton into their variables
#        if self.id not in added_pairings:
#            partner_id = self.participant.vars['other_player_group_id']
#            partner = self.group.get_player_by_id(partner_id)
#            partner_session_id = partner.id
#            # sort the player IDs
#            player_ids = sorted([self.id, partner_session_id])
#            # check if partnership already added
#            if partner_id not in added_pairings:
#                #partner_list.append(player_ids)
#                added_pairings.extend(player_ids)
#                self.session.vars['added_pairings'] = added_pairings
#                #self.session.vars['partner_list'] = partner_list
#            else:
#                print('partner id not in added_pairings')
        if timeout_happened:
            # Assign variables to timed out and kicked out
            self.timed_out = True
            self.participant.vars['timed_out_vote_outcome'] = True

class PartnerCheck(Page):
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
        #store partner variables
#        print("before storing partner variables")
#        for player in self.group.get_players():
#            if self.id_in_group == 1:
#                other_player = self.group.get_player_by_id(2)
#            elif self.id_in_group == 2:
#                other_player = self.group.get_player_by_id(1)
#            else:
#                print("no id in group for this player. Player group id:", self.id_in_group)
#            player.participant.vars['help_partner_group_id'] = other_player.id_in_group
#            player.participant.vars['help_partner_participant_id'] = other_player.participant.id_in_session
#        print("after storing partner variables")
#        self.participant.vars['other_policy_vote_description'] = 'in-office' if self.participant.vars[
#                                                                                    'other_policy_vote'] == 'Office' else 'remote'

        outcome = "remote" if self.remote_won == True else "office"
        vote = "remote" if self.participant.vars['policy_vote'] == "Remote" else "office"
        wonlost = "won" if self.winner == True else "lost"
        othervote = "remote" if self.treatment == 3 and self.remote_won == True else "office"

        return {
            'wonlost': wonlost,
            'vote': vote,
            'outcome': outcome,
            'othervote': othervote,
        }

    def before_next_page(self, timeout_happened):
        # timeout means that they give everything to their partner
        if timeout_happened:
            self.giving = 100
            self.participant.vars['giving'] = 100
            self.timed_out = True
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_partner_check'] = True

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'is_out' in self.participant.vars and self.participant.vars['is_out'] == 1:
            self.participant.vars['calculated_payoff'] = self.payoff
            return "payment_info"


class Offer(Page):
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
    form_fields = ["giving"]

    # custom error message if they did not select a number of points to give
    def error_message(player, values):
        if values['giving'] is None:
            return 'Please select the number of help points you want to give to your partner.'

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
        self.participant.vars['group_number'] = self.group_number
        if timeout_happened:
            self.giving = 100
            self.participant.vars['payoff'] = 0
            self.participant.vars['giving'] = self.giving
            self.participant.vars['timed_out'] = True
            self.participant.vars['timed_out_help'] = True
        else:
            self.finished_giving = True
            self.participant.vars['finished_giving'] = True

    # send those who are kicked out to the end of the experiment
    def app_after_this_page(self, upcoming_apps):
        if 'timed_out' in self.participant.vars and self.participant.vars['timed_out'] == 1:
            return "payment_info"
        else:
            return "PEQ"


page_sequence = [GroupAssignment, NoGroup, VoteOutcome, PartnerCheck, Offer]
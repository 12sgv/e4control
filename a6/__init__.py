from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
PAYMENT INFO
App 6/6 in sequence.
App Before: a5 (Survey)
App After: NONE, redirect to Prolific
---------------------------------------
Participants advance to this app after completing the survey (a5).
Participants are shown the breakdown of results and how much they earned from the study, unless they timed out.
Participants who completed the study are then allowed to provide feedback on the study.
Participants who completed the study are then redirected back to Prolific.
This app also hosts the code for the custom report screen for the Treatment condition.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a6'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    earnings = models.CurrencyField()
    feedback = models.LongStringField(
        label='''You may provide any feedback to the researchers here.''',
        blank=True,
    )
    finished = models.BooleanField(initial=False)
    completion_link = models.StringField()


# FUNCTIONS
def vars_for_admin_report(subsession):
    # initialize counters for the number of votes for each policy and winners/losers
    total_remote_votes = 0
    total_office_votes = 0
    total_voters = 0
    # initialize counters for participants assigned to each condition
    WL_participants_assigned = 0
    LW_participants_assigned = 0
    WW_participants_assigned = 0
    LL_participants_assigned = 0
    # initialize counters for the number of participants completed in each condition
    WL_participants_completed = 0
    LW_participants_completed = 0
    LL_participants_completed = 0
    WW_participants_completed = 0
    # Initialize counters for the number of participants finished in each condition
    WL_participants_finished = 0
    LW_participants_finished = 0
    LL_participants_finished = 0
    WW_participants_finished = 0
    # initialize a list of all payoffs for complete/not_paired/timed_out/
    completed_payments = []
    not_paired_payments = []
    timed_out_total = 0
    # initialize a list of all giving for each condition
    WW_giving = []
    LL_giving = []
    WL_giving = []
    LW_giving = []
    total_giving = []
    remote_giving = []
    office_giving = []
    # gather vars for the dashboard
    for player in subsession.get_players():
        # gather the votes for each policy
        if player.participant.vars.get('finished_voting') == True:
            total_voters += 1
            if player.participant.vars.get('policy_vote') == 'Remote':
                total_remote_votes += 1
            elif player.participant.vars.get('policy_vote') == 'Office':
                total_office_votes += 1
            # gather the assigned observations
            if player.participant.vars.get('treatment') == 1:
                WW_participants_assigned += 1
            elif player.participant.vars.get('treatment') == 2:
                LL_participants_assigned += 1
            elif player.participant.vars.get('treatment') == 3:
                WL_participants_assigned += 1
            elif player.participant.vars.get('treatment') == 4:
                LW_participants_assigned += 1
        # gather the completed observations
        if player.participant.vars.get('finished_giving') == True:
            total_giving.append(player.participant.vars.get('giving'))
            if player.participant.vars.get('policy_vote') == 'Remote':
                remote_giving.append(player.participant.vars.get('giving'))
            elif player.participant.vars.get('policy_vote') == 'Office':
                office_giving.append(player.participant.vars.get('giving'))
            if player.participant.vars.get('treatment') == 1:
                WW_participants_completed += 1
            elif player.participant.vars.get('treatment') == 2:
                LL_participants_completed += 1
            elif player.participant.vars.get('treatment') == 3:
                WL_participants_completed += 1
            elif player.participant.vars.get('treatment') == 4:
                LW_participants_completed += 1
        if player.participant.vars.get('finished') == True:
            # gather the finished observations and their giving
            if player.participant.vars.get('treatment') == 1:
                WW_participants_finished += 1
                WW_giving.append(player.participant.vars.get('giving'))
            elif player.participant.vars.get('treatment') == 2:
                LL_participants_finished += 1
                LL_giving.append(player.participant.vars.get('giving'))
            elif player.participant.vars.get('treatment') == 3:
                WL_participants_finished += 1
                WL_giving.append(player.participant.vars.get('giving'))
            elif player.participant.vars.get('treatment') == 4:
                LW_participants_finished += 1
                LW_giving.append(player.participant.vars.get('giving'))
            # gather payments for each type of participant (of the completed or not completed, but finished)
            if player.participant.vars.get('not_paired') == True:
                not_paired_payments.append(player.participant.vars.get('earnings'))
            else:
                completed_payments.append(player.participant.vars.get('earnings'))
                print("completed payment added", completed_payments)
        # count timed_out_participants
        if player.participant.vars.get('timed_out') == True:
            timed_out_total += 1

    # payment_data information
    payments_table_html = create_payments_table(subsession)

    # calculate the percentage of total votes that are for the 'Remote' policy and % that are losers
    total_votes = total_remote_votes + total_office_votes
    total_percent_votes_remote = round((total_remote_votes / total_votes) * 100, 2) if total_votes > 0 else 0

    # calculate the mean and total earnings for each group
    total_pay = sum(completed_payments) + sum(not_paired_payments)
    completed_payments_total = round(sum(completed_payments), 2)
    print(completed_payments_total, "Completed payments total")
    completed_payments_mean = round(sum(completed_payments) / len(completed_payments), 2) if len(
        completed_payments) > 0 else 0
    print("completed mean payment", completed_payments_mean)
    print("completed_payments list", completed_payments)
    not_paired_payments_total = sum(not_paired_payments)
    total_pay_mean = total_pay / (len(completed_payments) + len(not_paired_payments)) if len(
        not_paired_payments) > 0 or len(completed_payments) > 0 else 0

    # calculate the number of completed pairs vs timed out
    total_complete_finished = len(completed_payments)
    total_not_paired_finished = len(not_paired_payments)
    total_participants = total_voters
    percent_complete = round(100 * (total_complete_finished / total_participants), 2) if total_participants > 0 else 0
    percent_not_paired = round(100 * (total_not_paired_finished / total_participants),
                               2) if total_participants > 0 else 0
    percent_timed_out = round(100 * (timed_out_total / total_participants), 2) if total_participants > 0 else 0
    total_percent_completed = round(100 * ((total_complete_finished + total_not_paired_finished + timed_out_total) / total_participants), 2) if total_participants > 0 else 0

    # calculate the mean for each condition
    WW_mean = sum(WW_giving) / len(WW_giving) if len(WW_giving) > 0 else 0
    LL_mean = sum(LL_giving) / len(LL_giving) if len(LL_giving) > 0 else 0
    WL_mean = sum(WL_giving) / len(WL_giving) if len(WL_giving) > 0 else 0
    LW_mean = sum(LW_giving) / len(LW_giving) if len(LW_giving) > 0 else 0
    total_mean = sum(total_giving) / len(total_giving) if len(total_giving) > 0 else 0
    remote_mean = sum(remote_giving) / len(remote_giving) if len(remote_giving) > 0 else 0
    office_mean = sum(office_giving) / len(office_giving) if len(office_giving) > 0 else 0

    return dict(
        total_remote_votes=total_remote_votes, total_office_votes=total_office_votes,
        total_percent_votes_remote=total_percent_votes_remote,
        total_voters=total_voters,
        total_pay=total_pay, completed_payments_total=completed_payments_total,
        completed_payments_mean=completed_payments_mean, total_pay_mean=total_pay_mean,
        not_paired_payments_total=not_paired_payments_total,
        total_complete_finished=total_complete_finished, total_not_paired_finished=total_not_paired_finished,
        timed_out_total=timed_out_total, percent_complete=percent_complete, percent_timed_out=percent_timed_out,
        percent_not_paired=percent_not_paired, total_participants=total_participants,
        total_percent_completed = total_percent_completed,
        WW_participants_assigned=WW_participants_assigned, LL_participants_assigned=LL_participants_assigned,
        WL_participants_assigned=WL_participants_assigned, LW_participants_assigned=LW_participants_assigned,
        WW_participants_finished=WW_participants_finished, LL_participants_finished=LL_participants_finished,
        WL_participants_finished=WL_participants_finished, LW_participants_finished=LW_participants_finished,
        WW_participants_completed=WW_participants_completed, LL_participants_completed=LL_participants_completed,
        WL_participants_completed=WL_participants_completed, LW_participants_completed=LW_participants_completed,
        WW_mean=WW_mean, LL_mean=LL_mean, WL_mean=WL_mean, LW_mean=LW_mean,
        payments_table_html=payments_table_html,
        total_mean=total_mean, remote_mean=remote_mean, office_mean=office_mean,
    )


def get_participant_data(subsession):
    data = []
    for player in subsession.get_players():
        sessionid = player.participant.id
        participant_code = player.participant.code
        prolific_id = player.participant.label
        finished = player.participant.vars.get('finished', False)
        earnings = player.participant.vars.get('earnings', 0)
        data.append({
            'SessionID': sessionid,
            'Code': participant_code,
            'ProlificID': prolific_id,
            'Finished': finished,
            'earnings': earnings,
        })
    return data


def create_payments_table(subsession):
    data = get_participant_data(subsession)
    table_html = '''<style>
        th, td {
            text-align: center;
            min-width: 100px;
        }
    </style>
    <table>
        <tr>
            <th>SessionID</th>
            <th>Code</th>
            <th>ProlificID</th>
            <th>Finished</th>
            <th>Earnings</th>
        </tr>'''
    for participant in data:
        sessionID = participant['SessionID']
        code = participant['Code']
        prolific_id = participant['ProlificID']
        finished = 'Yes' if participant['Finished'] else 'No'
        finished_class = 'finished' if participant['Finished'] else ''
        earnings = participant['earnings']
        table_html += f'<tr class="{finished_class}"><td>{sessionID}</td><td>{code}</td><td>{prolific_id}</td><td>{finished}</td><td>${earnings:.2f}</td></tr>'
    table_html += '</table>'
    return table_html


# PAGES
#Main Group Payoff Page (Page 15)
class a61(Page):
    def is_displayed(self):
        if self.participant.vars['is_out'] == False and self.participant.vars['timed_out'] == False:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(self):
        participant = self.participant
        participant.vars['gave_dollars'] = cu(participant.vars['giving']) / 100
        participant.vars['kept_points'] = 100 - participant.vars['giving']
        participant.vars['kept_dollars'] = cu(participant.vars['kept_points']) / 100
        participant.vars['received_dollars'] = cu(participant.vars['other_giving']) / 100
        if self.participant.vars['winner']:
            self.earnings = self.session.config['participation_fee'] + self.session.config['initial_payoff_amount'] \
                            + self.session.config['outcome_payoff_effect'] + participant.vars['kept_dollars'] \
                            + participant.vars['received_dollars']
        else:
            self.earnings = self.session.config['participation_fee'] + self.session.config['initial_payoff_amount'] \
                            - self.session.config['outcome_payoff_effect'] + participant.vars['kept_dollars'] \
                            + participant.vars['received_dollars']
        self.participant.vars['earnings'] = self.earnings
        self.payoff = self.earnings
        outcome_effect = cu(self.session.config['outcome_payoff_effect'])
        initial_payoff_amount = cu(self.session.config['initial_payoff_amount'])

        return {
            'player_giving': participant.vars['giving'],
            'gave_dollars': participant.vars['gave_dollars'],
            'kept_points': participant.vars['kept_points'],
            'kept_dollars': participant.vars['kept_dollars'],
            'other_giving': participant.vars['other_giving'],
            'received_dollars': participant.vars['received_dollars'],
            'participation_fee': self.session.config['participation_fee'],
            'earnings': self.earnings,
            'outcome_effect': outcome_effect,
            'initial_payoff_amount': initial_payoff_amount,
        }

#2/3 Remote & 5th Person Payoff Page (Pages 16a & 16b)
class a62(Page):
    def is_displayed(self):
        if self.participant.vars['is_out'] == True and self.participant.vars['group_formation_timeout'] == 0:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        player.earnings = player.session.config['participation_fee'] + player.session.config['initial_payoff_amount'] + player.session.config['outcome_payoff_effect']
        player.participant.vars['earnings'] = player.earnings
        player.payoff = player.earnings
        outcome_effect = cu(player.session.config['outcome_payoff_effect'])
        initial_payoff_amount = cu(player.session.config['initial_payoff_amount'])
        not_paired_wording = "you were unable to be matched with a partner and were"
        return {
            'participation_fee': player.session.config['participation_fee'],
            'not_paired_wording': not_paired_wording,
            'extra_bonus': player.session.config['extra_bonus'],
            'outcome_effect': outcome_effect,
            'initial_payoff_amount': initial_payoff_amount,
            'earnings': player.earnings
        }

#Timed Out Group Formation Page
class a63(Page):
    def is_displayed(self):
        if self.participant.vars['group_formation_timeout'] == 1:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        player.earnings = player.session.config['participation_fee'] + player.session.config['extra_bonus']
        player.participant.vars['earnings'] = player.earnings
        player.payoff = player.earnings
        return {
            'participation_fee': player.session.config['participation_fee'],
            'extra_bonus': player.session.config['extra_bonus']
        }

#Timed Out Own Fault Page
class a64(Page):
    def is_displayed(self):
        if self.participant.vars['kicked_out'] == 1:
            return True
        else:
            return False


#End of Study Feedback Page (Page 17)
class a65(Page):
    form_model = 'player'
    form_fields = ['feedback']

    def is_displayed(self):
        if self.participant.vars['kicked_out'] == 1:
            return False
        else:
            return True

    def custom_export(players):
        yield ['id_in_session', 'winner_loser', 'pairing', ]

    @staticmethod
    def vars_for_template(self):
        self.finished = True
        self.participant.vars['finished'] = True
        # Assign completion codes
        if self.participant.vars['not_paired'] == True:
            self.completion_link = self.session.config['link_nopartner']
        elif self.participant.vars['group_formation_timeout'] == True:
            self.completion_link = self.session.config['link_timedoutgroup']
        elif self.participant.vars['kicked_out'] == True:
            self.completion_link = ""
        else:
            self.completion_link = self.session.config['link_completed']
        return {
            'earnings': self.earnings
        }


#Prolific Buffer Page
class a66(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['kicked_out'] == 1:
            return False
        else:
            return True

    @staticmethod
    def js_vars(player):
        return dict(completionlink=player.completion_link)
    pass


page_sequence = [a61, a62, a63, a64, a65, a66]

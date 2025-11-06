from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
PAYMENT INFO
App 4/4 in sequence.
App Before: a4 (PEQ)
App After: NONE, redirect to Prolific
---------------------------------------
Participants advance to this app after completing the survey (a4).
Participants are shown the breakdown of results and how much they earned from the study, unless they timed out.
Participants who completed the study are then allowed to provide feedback on the study.
Participants who completed the study are then redirected back to Prolific.
This app also hosts the code for the custom report screen for the Treatment condition.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a5'
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
    total_hybrid_votes = 0
    total_voters = 0
    # initialize a list of all payoffs for complete/not_paired/timed_out/
    completed_payments = []
    not_paired_payments = []
    timed_out_total = 0
    # initialize a list of all helping for each condition
    total_helping = []
    remote_helping = []
    hybrid_helping = []
    # gather vars for the dashboard
    for player in subsession.get_players():
        # gather the votes for each policy
        if player.participant.vars.get('finished') == True and player.participant.vars.get('is_out') == False:
            total_voters += 1
            if player.participant.vars.get('policy_vote') == 'Remote':
                total_remote_votes += 1
            elif player.participant.vars.get('policy_vote') == 'Hybrid':
                total_hybrid_votes += 1
        # gather the completed observations
        if player.participant.vars.get('finished') == True and player.participant.vars.get('is_out') == False:
            total_helping.append(player.participant.vars.get('helping'))
            if player.participant.vars.get('policy_vote') == 'Remote':
                remote_helping.append(player.participant.vars.get('helping'))
            elif player.participant.vars.get('policy_vote') == 'Hybrid':
                hybrid_helping.append(player.participant.vars.get('helping'))
        # gather payments for each type of participant (of the completed or not completed, but finished)
        if player.participant.vars.get('group_formation_timeout') == True:
            not_paired_payments.append(player.participant.vars.get('earnings'))
        elif player.participant.vars.get('finished') == True:
            completed_payments.append(player.participant.vars.get('earnings'))
            print("completed payment added", completed_payments)
        # count timed_out_participants
        if player.participant.vars.get('timed_out') == True:
            timed_out_total += 1

    # payment_data information
    payments_table_html = create_payments_table(subsession)

    # calculate the percentage of total votes that are for the 'Remote' policy and % that are losers
    total_votes = total_remote_votes + total_hybrid_votes
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
    total_mean = sum(total_helping) / len(total_helping) if len(total_helping) > 0 else 0
    remote_mean = sum(remote_helping) / len(remote_helping) if len(remote_helping) > 0 else 0
    hybrid_mean = sum(hybrid_helping) / len(hybrid_helping) if len(hybrid_helping) > 0 else 0

    return dict(
        total_remote_votes=total_remote_votes, total_hybrid_votes=total_hybrid_votes,
        total_percent_votes_remote=total_percent_votes_remote,
        total_voters=total_voters,
        total_pay=total_pay, completed_payments_total=completed_payments_total,
        completed_payments_mean=completed_payments_mean, total_pay_mean=total_pay_mean,
        not_paired_payments_total=not_paired_payments_total,
        total_complete_finished=total_complete_finished, total_not_paired_finished=total_not_paired_finished,
        timed_out_total=timed_out_total, percent_complete=percent_complete, percent_timed_out=percent_timed_out,
        percent_not_paired=percent_not_paired, total_participants=total_participants,
        total_percent_completed = total_percent_completed,
        payments_table_html=payments_table_html,
        total_mean=total_mean, remote_mean=remote_mean, hybrid_mean=hybrid_mean,
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
#Main Group Payoff Page (Page 14a and 14b)
class a51(Page):
    def is_displayed(self):
        if self.participant.vars['is_out'] == False and self.participant.vars['timed_out'] == False:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(self):
        participant = self.participant
        participant.vars['gave_dollars'] = cu(participant.vars['helping']) / 100
        print(participant.vars['other_helping'])
        participant.vars['received_dollars'] = cu(participant.vars['other_helping']) / 50
        print("other helping /50")
        print(participant.vars['other_helping'] / 50)
        self.earnings = self.session.config['participation_fee'] + self.session.config['initial_payoff_amount'] \
                            + participant.vars['received_dollars'] - participant.vars['gave_dollars']
        self.participant.vars['earnings'] = self.earnings
        self.payoff = self.earnings
        initial_payoff_amount = cu(self.session.config['initial_payoff_amount'])

        return {
            'player_helping': participant.vars['helping'],
            'gave_dollars': participant.vars['gave_dollars'],
            'other_helping': participant.vars['other_helping'],
            'received_dollars': participant.vars['received_dollars'],
            'participation_fee': self.session.config['participation_fee'],
            'earnings': self.earnings,
            'initial_payoff_amount': initial_payoff_amount,
        }


#Timed Out Group Formation (Page 14c)
class a52(Page):
    def is_displayed(self):
        if self.participant.vars['group_formation_timeout'] == 1:
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        player.earnings = player.session.config['participation_fee'] + player.session.config['initial_payoff_amount']
        player.participant.vars['earnings'] = player.earnings
        initial_payoff_amount = cu(player.session.config['initial_payoff_amount'])
        player.payoff = player.earnings
        return {
            'participation_fee': player.session.config['participation_fee'],
            'initial_payoff_amount': initial_payoff_amount,
        }

#Timed Out Own Fault Page (Page 15)
class a53(Page):
    def is_displayed(self):
        if self.participant.vars['kicked_out'] == 1:
            return True
        else:
            return False


#End of Study Feedback Page (Page 15a)
class a54(Page):
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
        if self.participant.vars['group_formation_timeout'] == True:
            self.completion_link = self.session.config['link_timedoutgroup']
        elif self.participant.vars['kicked_out'] == True:
            self.completion_link = ""
        else:
            self.completion_link = self.session.config['link_completed']
        return {
            'earnings': self.earnings
        }


#Prolific Buffer Page
class a55(Page):
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


page_sequence = [a51, a52, a53, a54, a55]

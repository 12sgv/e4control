from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
SURVEY
App 5/6 in sequence.
App Before: a3 (2/3 Remote) or a4 (PEQ)
App After: a6 (Payment Info)
---------------------------------------
Participants in the main group advance to this app after completing the PEQ (a4).
2/3 Remote participants complete this app after learning they have the shorter version of the study (a3)
All participants complete the survey. 
Participants answer basic demographic questions and questions about their work environment.
Then, all participants advance to the payment information app (a6).
"""


class C(BaseConstants):
    NAME_IN_URL = 'a5'
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = None
    StandardChoices = [
        [1, 'Strongly disagree'],
        [2, 'Moderately disagree'],
        [3, 'Slightly disagree'],
        [4, 'Neutral'],
        [5, 'Slightly agree'],
        [6, 'Moderately agree'],
        [7, 'Strongly agree'],
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
    InfluenceWorkTable = [
        'Not at all',
        '',
        'Slightly',
        '',
        'Moderately',
        '',
        'A great extent',
    ]

#may need to adjust the constants to allow for seamless code integration
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    is_out = models.BooleanField()
    is_bot = models.BooleanField()

# Demographics 1
    employed = models.IntegerField(choices=[
        [1, 'Full-time'],
        [2, 'Part-time'],
        [3, 'Not in paid work']],
        widget=widgets.RadioSelect,
        label='''What is your current employment status?''',
    )
    work_location = models.IntegerField(choices=[
        [1, '100% Remote'],
        [2, '100% In-person'],
        [3, 'Hybrid, mostly remote'],
        [4, 'Hybrid, mostly in-person']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes the policy where you <strong>currently</strong> work?''',
        blank=True,
    )
    location_preference = models.IntegerField(choices=[
        [1, '100% Remote'],
        [2, '100% In-person'],
        [3, 'Hybrid, mostly remote'],
        [4, 'Hybrid, mostly in-person']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes the policy under which you <strong>prefer</strong> to currently work?''',
    )
    education = models.IntegerField(choices=[
        [1, 'No formal qualifications'],
        [2, 'Secondary education'],
        [3, 'Technical/community college'],
        [4, 'Undergraduate degree'],
        [5, 'Graduate degree'],
        [6, 'Doctorate degree']],
        widget=widgets.RadioSelect,
        label='''Which of these is the highest level of education you have completed?'''
    )
    work_experience = models.IntegerField(label='How many years of work experience do you have?', min=0, max=80)
    firm_allow_input = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No'],
    ],
        widget=widgets.RadioSelect,
        label='Have you ever had an employer seek input from you and other employees on any work policies?',
    )
    remote_allow_input = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No'],
    ],
        widget=widgets.RadioSelect,
        blank=True,
        label='Has an employer sought employee input specifically on remote vs. hybrid work policies?')

# PAGES
class a51(Page):
    form_model = 'player'
    form_fields = [
        'employed', 'work_location', 'location_preference', 'education', 'work_experience',
        'firm_allow_input', 'remote_allow_input',
    ]

    def before_next_page(self, timeout_happened):
        self.participant.vars['employed'] = self.employed
        self.participant.vars['work_location'] = self.field_maybe_none('work_location')
        self.participant.vars['location_preference'] = self.location_preference
        self.participant.vars['education'] = self.education
        self.participant.vars['work_experience'] = self.work_experience
        self.participant.vars['firm_allow_input'] = self.firm_allow_input
        self.participant.vars['remote_allow_input'] = self.field_maybe_none('remote_allow_input')



page_sequence = [a51]

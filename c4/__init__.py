from otree.api import *
import time
from otree.export import get_fields_for_csv

doc = """
App 4/5 in sequence.
App Before: c2 (Help Task) or c3 (Vote Task)
App After: c5 (Payment Info)
---------------------------------------
Participants in the main group advance to this app after completing the Vote Task (c3).
5th participants arrive at this app after learning thei have the shorter version of the study (c2).
All participants complete the survey. 
Participants answer basic demographic questions and questions about their work environment.
Then, all participants advance to the payment information app (c5).
"""


class C(BaseConstants):
    NAME_IN_URL = 'c4'
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
        'None',
        '',
        '',
        'Some',
        '',
        '',
        'A lot',
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
        [3, 'Unemployed and job seeking'],
        [4, 'Not in paid work']],
        widget=widgets.RadioSelect,
        label='''What is your current employment status?''',
    )
    work_location = models.IntegerField(choices=[
        [1, '100% Remote'],
        [2, '100% In-person'],
        [3, 'Hybrid, mostly remote'],
        [4, 'Hybrid, mostly in-person'],
        [5, 'Other']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes the policy where you <strong>currently</strong> work?''',
    )
    location_preference = models.IntegerField(choices=[
        [1, '100% Remote'],
        [2, '100% In-person'],
        [3, 'Hybrid, mostly remote'],
        [4, 'Hybrid, mostly in-person'],
        [5, 'Other']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes the policy under which you <strong>prefer</strong> to work?''',
    )
    team_size = models.IntegerField(choices=[
        [1, 'I work by myself'],
        [2, 'I work with one other person'],
        [3, 'I work in a team of 3-5 people'],
        [4, 'I work in a team of 6-10 people'],
        [5, 'I work in a team of more than 10 people']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes your current team at work?''',
    )
    industry = models.IntegerField(choices=[
        [1, 'Financial services'],
        [2, 'Education'],
        [3, 'Health care'],
        [4, 'Information services'],
        [5, 'Food services'],
        [6, 'Legal services'],
        [7, 'Transportation'],
        [8, 'Other']],
        widget=widgets.RadioSelect,
        label='''Which of the following best describes your work industry?'''
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
        label='Has your current employer sought employee input on remote vs. in-office work policies?',
    )

    # Demographics 2
    firm_input = models.IntegerField(choices=[
        [1, 'Employee vote'],
        [2, 'Survey'],
        [3, 'One-on-one discussion'],
        [4, 'Town hall(s)'],
        [5, 'Apps like Slack or Teams'],
        [6, 'Other']],
        widget=widgets.RadioSelect,
        label='Please select the form of input your current employer sought from employees relating to remote vs. in-office work policies:',
    )
    firm_input_other = models.StringField(
        label='''If you selected 'Other' above, please describe how your current employer sought input:''',
        blank=True,
        initial='',
    )
    firm_feel_input = models.IntegerField(choices=[
        [1, 'None'],
        [2, ''],
        [3, ''],
        [4, 'Some'],
        [5, ''],
        [6, ''],
        [7, 'A lot']],
        label='''Please select the extent to which you feel that your input influenced your current employer's remote work policies:''',
        widget=widgets.RadioSelect,
    )
    firm_full_remote_pandemic = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No'],
    ],
        widget=widgets.RadioSelect,
        label='Did your current employer adopt a fully remote work policy during the pandemic?',
    )
    firm_adjust_post_pandemic = models.IntegerField(choices=[
        [1, 'No change, still fully-remote'],
        [2, 'Moved to hybrid, but mostly remote'],
        [3, 'Moved to hybrid, but in-office'],
        [4, 'Moved to fully in-office'],
    ],
        label='Has your current employer moved away from the fully remote policy adopted during the pandemic?',
        widget=widgets.RadioSelect,
        blank=True,
    )


# PAGES
#12. First page of Demographics Survey
class c41(Page):
    form_model = 'player'
    form_fields = [
        'employed', 'work_location', 'location_preference', 'team_size', 'industry', 'education', 'work_experience',
        'firm_allow_input',
    ]

    def before_next_page(self, timeout_happened):
        self.participant.vars['employed'] = self.employed
        self.participant.vars['work_location'] = self.work_location
        self.participant.vars['location_preference'] = self.location_preference
        self.participant.vars['team_size'] = self.team_size
        self.participant.vars['industry'] = self.industry
        self.participant.vars['education'] = self.education
        self.participant.vars['work_experience'] = self.work_experience
        self.participant.vars['firm_allow_input'] = self.firm_allow_input

#13. Second Page of Demographics Survey
class c42(Page):
    form_model = 'player'
    form_fields = [
        'firm_input', 'firm_input_other', 'firm_feel_input',
        'firm_full_remote_pandemic', 'firm_adjust_post_pandemic',
    ]

    def is_displayed(self):
        if self.firm_allow_input == True:
            self.participant.vars['firm_allow_input'] = True
            return True
        else:
            return False

    def before_next_page(self, timeout_happened):
        self.participant.vars['firm_input'] = self.firm_input
        self.participant.vars['firm_input_other'] = self.firm_input_other
        self.participant.vars['firm_feel_input'] = self.firm_feel_input
        self.participant.vars['firm_full_remote_pandemic'] = self.firm_full_remote_pandemic
        self.participant.vars['firm_adjust_post_pandemic'] = self.field_maybe_none('firm_adjust_post_pandemic')


page_sequence = [c41, c42]

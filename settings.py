from os import environ


SESSION_CONFIGS = [
       dict(
        name='control',
        app_sequence=['a1', 'a2', 'a4', 'a5'],
        num_demo_participants=5,
        use_browser_bots=False,
       ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01,
    participation_fee=1.50,
    initial_payoff_amount=1.10,
    outcome_payoff_effect=0.50,
    doc="",
    debug=False,
    group_size=5,
    group_formation_timeout=420,
    additional_instructions_timeout=60,
    offer_timeout=185,
    help_wait_timeout=260,
    link_completed='https://app.prolific.com/submissions/complete?cc=CZJVIYO8',
    link_timedoutgroup='https://app.prolific.com/submissions/complete?cc=CC7X771N',
   )

PARTICIPANT_FIELDS = [
    'ProlificID',
    'policy_vote', 'hybrid_votes', 'remote_votes',
    'winning_policy', 'policy_vote_result', 'earnings', 'pairing',
    'pair_number', 'giving', 'other_giving', 'dollar_payoff',
    'participant_code', 'participant_id', 'prolific_id',
    'age', 'race', 'education', 'employed', 'work_experience',
    'work_location', 'team_size', 'industry', 'firm_policy',
    'firm_voice', 'remote_preference', 'office_preference',
    'vote_preference', 'positive_affect', 'negative_affect',
    'group_id1', 'group_id2', 'group_id3', 'group_id4', 'group_id5',
    'offer_finished', 'other_player', 'other_similar', 'other_policy_vote',
    'completion_code',

]
SESSION_FIELDS = [
    'num_winner_winner_pairs',
    'num_winner_loser_pairs',
    'num_loser_loser_pairs',
    'unique_pairings',
    'group_number',
    'group_type',
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='live_instrument',
        display_name='live_instrument',
    ),
    dict(name='practice_room',
         display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

#Environemnt Variables
OTREE_AUTH_LEVEL = 'STUDY'
#OTREE_AUTH_LEVEL can either be STUDY (only links provided can access) or DEMO (anyone can use it)
OTREE_PRODUCTION = 1
#OTREE_PRODUCTION is either 1 or 0 where 1 is production mode on

DEMO_PAGE_INTRO_HTML = """
Econ version of my first year paper.
"""


SECRET_KEY = '8439773646795'

INSTALLED_APPS = ['otree']

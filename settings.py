from os import environ
import os

SESSION_CONFIGS = [
    dict(name='inno_teams', app_sequence=['intro', 'task_1', 'video_chat'], num_demo_participants=6),
    dict(name='test', app_sequence=['video_chat'], num_demo_participants=6)
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['order', 'partner', 'overallprofit','overallpayoffrealworld', 'finallocation','finalprofit',
                      'maxprofit','locdefault','locdefaulth1','locdefaulth2', 'stdvsugar', 'stdvlemon', 'stdvprice',
                      'stdvprice', 'stdvsugarh1','stdvlemonh1','stdvpriceh1','stdvsugarh2', 'stdvlemonh2',
                      'stdvpriceh2','stdvprofit','stdvprofith1','stdvprofith2','maxexpphase','durexpphase', 'initial_sugar', 'treat_video',
                      'partner', 'team_name', 'pair','group6mem']
SESSION_FIELDS = ['num_groups']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

EXTENSION_APPS = ['otree_tools']

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """



SECRET_KEY = '1564016201268'

ROOMS = [
    dict(name=f'test{x}', display_name=f'test{x}', participant_label_file="labels.txt")
    for x in range(1, 40)
]

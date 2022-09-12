from os import environ
import os

SESSION_CONFIGS = [
    dict(name='test', app_sequence=['video_chat'], num_demo_participants=6)
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['order', 'partner', 'overallprofit', 'finallocation','finalprofit','treat_video',
                      'partner', 'team_name', 'pair','group6mem', 'image_data', 'name']
SESSION_FIELDS = ['num_groups']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

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

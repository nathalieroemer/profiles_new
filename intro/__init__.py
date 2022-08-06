from otree.api import *
import requests
import random
import itertools

doc = """
Introduction
"""

class Constants(BaseConstants):
    name_in_url = 'lemonade'
    players_per_group = None
    num_rounds = 1
    instructions_template10 = 'intro/Instructions10.html'
    instructions_template20 = 'intro/Instructions20.html'
    instructions_template30 = 'intro/Instructions30.html'
    instructions_template40 = 'intro/Instructions40.html'
    instructions_template50 = 'intro/Instructions50.html'


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    name = models.StringField()

    a1 = models.IntegerField(
        verbose_name='What percentage of the total lemonade stand profit will you earn?', )

    a2 = models.IntegerField(choices=[
        [1, '1'],
        [2, '10'],
        [3, '100'],
    ],
        verbose_name='100 thaler are worth €:',
        widget=widgets.RadioSelect)


    a4 = models.IntegerField(
        verbose_name='What percentage of the total lemonade stand profit will you earn?', )

    a5 = models.IntegerField(choices=[
        [1, '1'],
        [2, '10'],
        [3, '100'],
    ],
        verbose_name='100 thaler are worth €:',
        widget=widgets.RadioSelect)


class Welcome(Page):
    pass

class Info(Page):
    form_model = 'player'
    form_fields = ['name']

class Introduction10(Page):
    pass

class Introduction20(Page):
    pass

class Introduction30(Page):
    pass

class Introduction40(Page):
    pass


class Introduction60(Page):
    form_model = 'player'
    form_fields = ['a1','a2']
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(player):
        pass

class Results(Page):
    pass

page_sequence = [
 Welcome, Info, Introduction10, Introduction20, Introduction30, Introduction40, Introduction60
]



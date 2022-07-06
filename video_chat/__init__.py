from otree.api import *
import requests

doc = """
Video chat between 2 players
"""


class Constants(BaseConstants):
    name_in_url = 'webcam'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
   recording = models.StringField()



# PAGES
class Call1(Page):
    @staticmethod
    def live_method(player, data):
        player.recording = data['value']
        if 'video_chat' in data:
            return {3 - player.id_in_group: data}

class Last(Page):
    pass

page_sequence = [Call1, Last]

from otree.api import *
from django.contrib.staticfiles.templatetags.staticfiles import static
import io
import os
import re
import base64
import requests
from PIL import Image
from django.conf import settings
from uuid import uuid4
dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
from random import seed
from random import randint

doc = """
Video chat between 2 players
"""


class Constants(BaseConstants):
    name_in_url = 'profile_picture'
    players_per_group = None
    num_rounds = 1
    IMAGE_EXTENTION = 'png'


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    full_path_to_image = models.LongStringField()
    image_info = models.LongStringField()
    pic_id = models.StringField()
    image_data = models.StringField()
    video = models.IntegerField()


class Instructions(Page):
    pass

    def before_next_page(player, timeout_happened):
        player.pic_id = "xyz"

class takepic(Page):
    form_model= 'player'
    form_fields = ['image_info']

    # hier wird das bild gemacht und hochgeladen

    def before_next_page(player, timeout_happened):
        import os
        ImageData = player.image_info
        ImageData = dataUrlPattern.match(ImageData).group(2)
        player.image_data = ImageData
        i = base64.b64decode(ImageData)
        im = Image.open(io.BytesIO(i))
        base_dir = os.path.dirname(os.path.abspath(__file__))
        your_media_root = os.path.join(base_dir, 'media')
        file_name = player.pic_id
        path_to_file = os.path.join(your_media_root, f'{file_name}.{Constants.IMAGE_EXTENTION}')
        im.save(path_to_file)
        player.full_path_to_image = path_to_file


class Promotion(Page):
    def vars_for_template(player):
        pic_1 = player.image_data
        return dict(photo1=pic_1)


class Last(Page):
    pass

page_sequence = [Instructions, takepic, Promotion]


from otree.api import *
import requests

doc = """
Video chat between 2 players
"""


class Constants(BaseConstants):
    name_in_url = 'webcam'
    players_per_group = 6
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
   recording = models.StringField()
   pref1 = models.IntegerField()
   pref2 = models.IntegerField()
   pref3 = models.IntegerField()
   pref4 = models.IntegerField()
   pref5 = models.IntegerField()
   pref6 = models.IntegerField()
   name = models.StringField()

class Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        import random
        participant = player.participant
        participant.order = [1,2,3,4,5,6]
        participant.order.remove(player.id_in_group)
        random.shuffle(participant.order)

        print(participant.order)

# PAGES
class Call1(Page):
    #timeout_seconds = 30
    @staticmethod
    def live_method(player, data):
        player.recording = data['value']
        if 'video_chat' in data:
            ## get the others data
            if player.id_in_group == 1:
                return {2: data}
            if player.id_in_group == 2:
                return {1: data}

            if player.id_in_group == 3:
                return {4: data}
            if player.id_in_group == 4:
                return {3: data}

            if player.id_in_group == 5:
                return {6: data}
            if player.id_in_group == 6:
                return {5: data}

class WaitPage1(WaitPage):
    pass

class Call2(Page):
    #timeout_seconds = 30
    @staticmethod
    def live_method(player, data):
        player.recording = data['value']
        if 'video_chat' in data:
            ## get the others data
            if player.id_in_group == 1:
                return {6: data}
            if player.id_in_group == 6:
                return {1: data}

            if player.id_in_group == 3:
                return {2: data}
            if player.id_in_group == 2:
                return {3: data}

            if player.id_in_group == 5:
                return {4: data}
            if player.id_in_group == 4:
                return {5: data}

class WaitPage2(WaitPage):
    pass

class Call3(Page):
    #timeout_seconds = 60
    @staticmethod
    def live_method(player, data):
        player.recording = data['value']
        if 'video_chat' in data:
            ## get the others data
            if player.id_in_group == 1:
                return {4: data}
            if player.id_in_group == 4:
                return {1: data}

            if player.id_in_group == 3:
                return {6: data}
            if player.id_in_group == 6:
                return {3: data}

            if player.id_in_group == 5:
                return {2: data}
            if player.id_in_group == 2:
                return {5: data}

class Preferences2(Page):
    form_model = 'player'
    form_fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5', 'pref6']

    def vars_for_template(player):
        pref = "pref"
        participant = player.participant
        order = participant.order
        print(order)
        p1 = player.group.get_player_by_id(1)
        p2 = player.group.get_player_by_id(2)
        p3 = player.group.get_player_by_id(3)
        p4 = player.group.get_player_by_id(4)
        p5 = player.group.get_player_by_id(5)
        p6 = player.group.get_player_by_id(6)

        self = player.id_in_group
        return dict(
            order=order,
            p1 = p1, p2 = p2, p3=p3, p4=p4, p5=p5, p6=p6, self=self)

class WaitPage3(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p3 = group.get_player_by_id(3)
            p4 = group.get_player_by_id(4)
            p5 = group.get_player_by_id(5)
            p6 = group.get_player_by_id(6)
           # matches_p1 =  [dict(member=2, weight=p1.pref2 + p2.pref1), dict(member=3, weight=p1.pref3 + p3.pref1), dict(member=4, weight=p1.pref4 + p4.pref1),
           #                dict(member=5, weight=p1.pref5 + p5.pref1), dict(member=6, weight=p1.pref6 + p6.pref1)]
            matches_p1 = {2: p1.pref2 + p2.pref1, 3: p1.pref3 + p3.pref1, 4: p1.pref4 + p4.pref1,
                           5: p1.pref5 + p5.pref1, 6: p1.pref6 + p6.pref1 }
            print(matches_p1)
            match_p1 = max(matches_p1, key=matches_p1.get)
            print("Maximum value:", match_p1)
            for p in group.get_players():
                participant = p.participant
                if p.id_in_group == 1:
                    participant.partner = match_p1
                else:
                    participant.partner = 0

            print(p.participant.partner)


        ## get participantid of gorup member p2 and store it as particpant variable for member 1 to have their matches




class Last(Page):
    pass

page_sequence = [Instructions, Call1, WaitPage1, Call2, WaitPage2, Call3, WaitPage3, Last]
#page_sequence = [WaitPage1, Preferences2, WaitPage3, Last]

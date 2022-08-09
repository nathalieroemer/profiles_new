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

def creating_session(subsession):
    import itertools
    if subsession.round_number == 1:
        treat = itertools.cycle([1, 0])
        num_group_ids = []
        for group in subsession.get_groups():
            group.treat_video = next(treat)
            num_group_ids.append(group.id_in_subsession)
            group.session.num_groups = max(num_group_ids)
            print(group.session.num_groups, "this is the number of groups")
            for player in group.get_players():
                participant = player.participant
                participant.treat_video = group.treat_video

class Group(BaseGroup):
    treat_video = models.IntegerField()


class Player(BasePlayer):
   recording = models.StringField()
   pref1 = models.IntegerField()
   pref2 = models.IntegerField()
   pref3 = models.IntegerField()
   pref4 = models.IntegerField()
   pref5 = models.IntegerField()
   pref6 = models.IntegerField()
   name = models.StringField()
   team = models.IntegerField()


class Instructions(Page):
    form_model = 'player'
    form_fields = ['name']
    @staticmethod
    def before_next_page(player, timeout_happened):
        import random
        participant = player.participant
        participant.order = [1,2,3,4,5,6]
        participant.order.remove(player.id_in_group)
        random.shuffle(participant.order)
        participant.group6mem = player.group.id_in_subsession

        print(participant.order)

# PAGES
class Call1(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.treat_video ==1

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
    @staticmethod
    def is_displayed(player):
        return player.group.treat_video ==1


class Call2(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.treat_video ==1

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
    @staticmethod
    def is_displayed(player):
        return player.group.treat_video ==1


class Call3(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.treat_video ==1

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

            ## generate list of all possible combinations
            import itertools
            participants = [1, 2, 3, 4, 5, 6]
            list_pairings = []
            list_prefsum = []
            for pair in itertools.permutations(participants, 2):
                print(pair)
                list_pairings.append(pair)
                p = "p"
                pref = "pref"
                summant1 = p + str(pair[0]) + "." + pref + str(pair[1])
                summant2 = p + str(pair[1]) + "." + pref + str(pair[0])
                sum = eval(summant1) + eval(summant2)
                print("sum is", sum)
                list_prefsum.append(sum)
                print(list_prefsum, "list prefsums")
                print(list_pairings)

                # generate dictionary with pairs (key) and their preference sums (dictionary)
            dict_matches = dict(zip(list_pairings, list_prefsum))
            print("dict is", dict_matches)
            teams_list = []
            teams_prefs = []
            num_teams = 0
            while num_teams < 3:
                print("old dict", dict_matches)
                max_value = max(dict_matches, key=dict_matches.get)
                match_value = dict_matches[max_value]
                teams_prefs.append(match_value)
                print(match_value, "preference sum")
                teams_list.append(max_value)
                print(max_value[0])
                ## delete all entries in which either the first or the second member of the new team is in (so all combinations containing these two members)
                dict_matches = {k:v for k,v in dict_matches.items() if not max_value[0] in k}
                dict_matches = {k: v for k, v in dict_matches.items() if not max_value[1] in k}
                print("new dict", dict_matches)
                num_teams = len(teams_list)
            print(teams_list, "list of teams")

            print(teams_prefs, "list of preferences")

            for tupel in teams_list:
                for p in group.get_players():
                    participant = p.participant
                    if tupel[0] == p.id_in_group:
                        participant.pair = tupel
                        participant.partner = tupel[1]
                        p.team = tupel[1]
                        print(p.team,"team member is")
                        print(participant.partner)
                    if tupel[1] == p.id_in_group:
                        participant.partner = tupel[0]
                        participant.pair = tupel
                        p.team = tupel[0]
                        print(p.team, "is member of the team")
                    else:
                        pass

            team1 = teams_list[0]
            team2 = teams_list[1]
            team3 = teams_list[2]
            for p in group.get_players():
            ## check if this works with multiple groups
                participant = p.participant
                if team1[1] or team1[0] ==p.id_in_group:
                    participant.team_name = "team1_s" + str(p.group.id_in_subsession)
                    print(participant.team_name)
                if team2[1] or team2[0] ==p.id_in_group:
                    participant.team_name = "team2_s" + str(p.group.id_in_subsession)
                    print(participant.team_name)
                if team3[1] or team3[0] ==p.id_in_group:
                    participant.team_name = "team2_s" + str(p.group.id_in_subsession)
                    print(participant.team_name)

class Last(Page):
    pass

#page_sequence = [Instructions, Call1, WaitPage1, Call2, WaitPage2, Call3, WaitPage3, Last]
page_sequence = [Instructions, WaitPage1, Preferences2, WaitPage3, Last]

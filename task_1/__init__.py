from otree.api import *
import requests
import statistics


doc = """
Introduction
"""

class Constants(BaseConstants):
    name_in_url = 'task_1'
    players_per_group = None
    num_rounds = 5
    BusinessDemand = 100
    SchoolDemand = 200
    StadiumDemand = 60
    #Bliss points for each location
    BusinessSugar = 1.55
    BusinessLemon = 7.55
    BusinessLemonadeColor = 1
    BusinessPrice = 7.55
    SchoolSugar = 9.55
    SchoolLemon = 1.55
    SchoolLemonadeColor = 2
    SchoolPrice = 2.55
    StadiumSugar = 5.55
    StadiumLemon = 5.55
    StadiumLemonadeColor = 1
    StadiumPrice = 7.55
    #Penalties for each location
    BusinessSugarPenalty = 3
    BusinessLemonPenalty = 3
    BusinessLemonadeColorPenalty = 20
    BusinessPricePenalty = 3
    SchoolSugarPenalty = 6
    SchoolLemonPenalty = 6
    SchoolLemonadeColorPenalty = 60
    SchoolPricePenalty = 6
    StadiumSugarPenalty = 0.5
    StadiumLemonPenalty = 0.5
    StadiumLemonadeColorPenalty = 0.5
    StadiumPricePenalty = 0.5
    SugarLow = "Some of your customers told you that the lemonade is not sweet enough."
    SugarHigh = "Some of your customers told you that the lemonade is too sweet."
    LemonLow = "Some of your customers told you that the lemonade is not sour/acidic enough."
    LemonHigh = "Some of your customers told you that the lemonade is too sour/acidic."
    PriceLow = "You have too many customers demanding lemonade. The price may be too low."
    PriceHigh = "You have too few customers demanding lemonade. The price may be too high."

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField(blank=True)
    location = models.IntegerField(
        choices=[
            (1, 'Business District'),
            (2, 'School'),
            (3, 'Stadium'),
        ],
        verbose_name='Location of your stand:',
        widget=widgets.RadioSelectHorizontal)
    color = models.IntegerField(
        choices=[
            (1, 'Green'),
            (2, 'Pink'),
        ],
        verbose_name='Lemonade color:',
        widget=widgets.RadioSelectHorizontal)

    sugar = models.FloatField(
        min=0, max=20,
        verbose_name='Sugar content (in %):',
       #   widget=widgets.NumberWidget(attrs={'step': '0.1'}),
    )

    lemon = models.FloatField(
        min=0, max=20,
        verbose_name='Lemon content (in %):',
      #  widget=widgets.NumberInput(attrs={'step': '0.1'}),
    )

    price = models.FloatField(
        # min=c(0.0), max=c(10.0),
        verbose_name='Price of one cup (in thaler):',
        min=0.1, max=10,
        # currency_range=(c(0), c(10), c(0.1))
        # currency_range(c(0), c(0.10), c(0.02))
       # widget=widgets.NumberInput(attrs={'step': '0.1'}),
    )
    random_customer = models.FloatField(doc="creating a random variable to determine customer feedback")
    profit = models.CurrencyField(doc="profit of the lemonade stand, in thalers")
    maxexpphase = models.IntegerField(doc="maximal duration of a exploratory phase")
    durexpphase = models.IntegerField(doc="total duration of all exploratory phases")
    report = models.LongStringField(doc="text of reporting field, free form text subjects reported", verbose_name='',
                                    blank=True)
    reportlength = models.IntegerField(doc="length of reported text")


    # TO INCLUDE STANDARD DEVIATIONS from ROUND TO ROUND.
    def set_profit(player):
        import random
        player.random_customer = round((random.random()), 3)  # assign random value for feedback
        if player.location == 1:
            SugarPenalty = abs(Constants.BusinessSugar - player.sugar) * Constants.BusinessSugarPenalty
            LemonPenalty = abs(Constants.BusinessLemon - player.lemon) * Constants.BusinessLemonPenalty
            ColorPenalty = abs(
                Constants.BusinessLemonadeColor - player.color) * Constants.BusinessLemonadeColorPenalty
            PricePenalty = abs(Constants.BusinessPrice - player.price) * Constants.BusinessPricePenalty
            TotalPenalty = SugarPenalty + LemonPenalty + ColorPenalty + PricePenalty
            if Constants.BusinessDemand - TotalPenalty > 0:
                player.profit = Constants.BusinessDemand - TotalPenalty
            else:
                player.profit = 0

        if player.location == 2:
            SugarPenalty = abs(Constants.SchoolSugar - player.sugar) * Constants.SchoolSugarPenalty
            LemonPenalty = abs(Constants.SchoolLemon - player.lemon) * Constants.SchoolLemonPenalty
            ColorPenalty = abs(
                Constants.SchoolLemonadeColor - player.color) * Constants.SchoolLemonadeColorPenalty
            PricePenalty = abs(Constants.SchoolPrice - player.price) * Constants.SchoolPricePenalty
            TotalPenalty = SugarPenalty + LemonPenalty + ColorPenalty + PricePenalty
            if Constants.SchoolDemand - TotalPenalty > 0:
                player.profit = Constants.SchoolDemand - TotalPenalty
            else:
                player.profit = 0

        if player.location == 3:
            SugarPenalty = abs(Constants.StadiumSugar - player.sugar) * Constants.StadiumSugarPenalty
            LemonPenalty = abs(Constants.StadiumLemon - player.lemon) * Constants.StadiumLemonPenalty
            ColorPenalty = abs(
                Constants.StadiumLemonadeColor - player.color) * Constants.StadiumLemonadeColorPenalty
            PricePenalty = abs(Constants.StadiumPrice - player.price) * Constants.StadiumPricePenalty
            TotalPenalty = SugarPenalty + LemonPenalty + ColorPenalty + PricePenalty
            if Constants.StadiumDemand - TotalPenalty > 0:
                player.profit = Constants.StadiumDemand - TotalPenalty
            else:
                player.profit = 0

    def set_payoff(player):
        player.payoff = (player.profit * 0.5)


    def set_expphase(player):
        if player.location == 1:
            player.maxexpphase = 0
            player.durexpphase = 0
        else:
            if player.round_number == 1:
                player.maxexpphase = 1
                player.durexpphase = 1
            else:
                if player.location == player.in_round(player.round_number - 1).location and player.color == player.in_round(
                        player.round_number - 1).color and (
                        abs(player.sugar - player.in_round(player.round_number - 1).sugar) < 0.25) and \
                        (abs(player.lemon - player.in_round(player.round_number - 1).lemon) < 0.25) and (
                        abs(player.price - player.in_round(
                            player.round_number - 1).price) < 0.25):
                    player.maxexpphase = 0
                    player.durexpphase = 0
                else:
                    player.maxexpphase = (1 + player.in_round(player.round_number - 1).maxexpphase)
                    player.durexpphase = 1

    def feedback(player):
        if player.location == 1:
            if player.random_customer <= (1 / 3):  # FEEDBACK ON SUGAR
                if (Constants.BusinessSugar - player.sugar) > 0:
                    return Constants.SugarLow
                else:
                    return Constants.SugarHigh
            else:
                pass
            if (1 / 3) < player.random_customer <= (2 / 3):  # FEEDBACK ON LEMON
                if (Constants.BusinessLemon - player.lemon) > 0:
                    return Constants.LemonLow
                else:
                    return Constants.LemonHigh
            else:
                pass

            if player.random_customer > (2 / 3):  # FEEDBACK ON PRICE
                if (Constants.BusinessPrice - player.price) > 0:
                    return Constants.PriceLow
                else:
                    return Constants.PriceHigh
            else:
                pass

        if player.location == 2:
            if player.random_customer <= (1 / 3):  # FEEDBACK ON SUGAR
                if (Constants.SchoolSugar - player.sugar) > 0:
                    return Constants.SugarLow
                else:
                    return Constants.SugarHigh
            else:
                pass
            if (1 / 3) < player.random_customer <= (2 / 3):  # FEEDBACK ON LEMON
                if (Constants.SchoolLemon - player.lemon) > 0:
                    return Constants.LemonLow
                else:
                    return Constants.LemonHigh
            else:
                pass

            if player.random_customer > (2 / 3):  # FEEDBACK ON PRICE
                if (Constants.SchoolPrice - player.price) > 0:
                    return Constants.PriceLow
                else:
                    return Constants.PriceHigh
            else:
                pass

        if player.location == 3:
            if player.random_customer <= (1 / 3):  # FEEDBACK ON SUGAR
                if (Constants.StadiumSugar - player.sugar) > 0:
                    return Constants.SugarLow
                else:
                    return Constants.SugarHigh
            else:
                pass

            if (1 / 3) < player.random_customer <= (2 / 3):  # FEEDBACK ON LEMON
                if (Constants.StadiumLemon - player.lemon) > 0:
                    return Constants.LemonLow
                else:
                    return Constants.LemonHigh
            else:
                pass

            if player.random_customer > (2 / 3):  # FEEDBACK ON PRICE
                if (Constants.StadiumPrice - player.price) > 0:
                    return Constants.PriceLow
                else:
                    return Constants.PriceHigh
            else:
                pass

    def vars_for_template(player):
        return {
            'period1': player.round_number - 2,
            'period2': player.round_number - 1,
            'period3': player.round_number,
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['location', 'sugar', 'lemon', 'color', 'price']

    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            location = 1
            sugar = 5.2
            lemon = 7.0
            color = 1
            price = 8.2
            return dict(sugar=sugar,
                        location=location,
                        lemon=lemon,
                        color=color,
                        price=price)
        if player.round_number > 1:
            sugar = player.in_round(player.round_number - 1).sugar
            location = player.in_round(player.round_number - 1).location
            lemon = player.in_round(player.round_number - 1).lemon
            color = player.in_round(player.round_number - 1).color
            price = player.in_round(player.round_number - 1).price
            return dict(sugar=sugar,
                        location=location,
                        lemon=lemon,
                        color=color,
                        price=price)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.set_profit()
        player.set_payoff()
        player.feedback()
        player.set_expphase()


class Results(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.round_number == Constants.num_rounds:
            ## TODO: can they be replaced by regular player. variables?
            last_round = Constants.num_rounds
            participant.overallprofit = sum([p.profit for p in player.in_all_rounds()])
            participant.overallpayoffrealworld= cu(participant.payoff_plus_participation_fee())
            participant.finallocation = player.in_round(last_round).location
            participant.finalprofit = player.in_round(last_round).profit
            participant.maxprofit = max([p.profit for p in player.in_all_rounds()])
            participant.locdefault = ([p.location for p in player.in_all_rounds()]).count(1) #self.player.locnotdefault.in_all_rounds().count(True)
            participant.locdefaulth1= ([p.location for p in player.in_rounds(1, last_round)]).count(1)
#            participant.locdefaulth2 = ([p.location for p in player.in_rounds(11, 20)]).count(1)
            participant.stdvsugar = statistics.stdev(([p.sugar for p in player.in_all_rounds()]),
                                                                  xbar=(statistics.mean(
                                                                      [p.sugar for p in player.in_all_rounds()])))
            participant.vars['stdvlemon'] = statistics.stdev(([p.lemon for p in player.in_all_rounds()]),
                                                                  xbar=(statistics.mean(
                                                                      [p.lemon for p in player.in_all_rounds()])))
            participant.vars['stdvprice'] = statistics.stdev(([p.price for p in player.in_all_rounds()]),
                                                                  xbar=(statistics.mean(
                                                                      [p.price for p in player.in_all_rounds()])))
            participant.vars['stdvsugarh1'] = statistics.stdev(([p.sugar for p in player.in_rounds(1,last_round)]),
                                                                    xbar=(statistics.mean(
                                                                        [p.sugar for p in player.in_rounds(1,last_round)])))
            participant.vars['stdvlemonh1'] = statistics.stdev(([p.lemon for p in player.in_rounds(1,last_round)]),
                                                                  xbar=(statistics.mean(
                                                                      [p.lemon for p in player.in_rounds(1,last_round)])))
            participant.vars['stdvpriceh1'] = statistics.stdev(([p.price for p in player.in_rounds(1,last_round)]),
                                                                  xbar=(statistics.mean(
                                                                      [p.price for p in player.in_rounds(1,last_round)])))
#            participant.vars['stdvsugarh2'] = statistics.stdev(([p.sugar for p in player.in_rounds(11,20)]),
#                                                                    xbar=(statistics.mean(
#                                                                        [p.sugar for p in player.in_rounds(11,20)])))
#            participant.vars['stdvlemonh2'] = statistics.stdev(([p.lemon for p in player.in_rounds(11,20)]),
#                                                                  xbar=(statistics.mean(
#                                                                      [p.lemon for p in player.in_rounds(11,20)])))
#            participant.vars['stdvpriceh2'] = statistics.stdev(([p.price for p in player.in_rounds(11,20)]),
#                                                                  xbar=(statistics.mean(
#                                                                      [p.price for p in player.in_rounds(11,20)])))
            participant.vars['stdvprofit'] = statistics.stdev(
                ([p.profit for p in player.in_all_rounds()]),
                xbar=(statistics.mean(
                    [p.profit for p in player.in_all_rounds()])))
            participant.vars['stdvprofith1'] = statistics.stdev(
                ([p.profit for p in player.in_rounds(1, last_round)]),
                xbar=(statistics.mean(
                    [p.profit for p in player.in_rounds(1, last_round)])))
#            participant.vars['stdvprofith2'] = statistics.stdev(
#                ([p.profit for p in player.in_rounds(11,20)]),
#                xbar=(statistics.mean(
#                    [p.profit for p in player.in_rounds(11,20)])))
            participant.vars['maxexpphase']= max([p.maxexpphase for p in player.in_all_rounds()])
            participant.vars['durexpphase']= sum([p.durexpphase for p in player.in_all_rounds()])
        else:
            pass

## TODO: think about whether to include this in some form
class Report(Page):
    form_model = 'player'
    form_fields = ['report']

    @staticmethod
    def is_displayed(player):
       if (player.round_number == 3) or (player.round_number == 6 ) or (player.round_number == 9) or (
                player.round_number == 12):
           return True
       else:
            return False

    @staticmethod
    def vars_for_template(player):
        return player.vars_for_template()

page_sequence = [Decision,Results
]

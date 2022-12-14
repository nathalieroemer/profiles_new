from otree.api import *
import requests

doc = """
Video chat between 2 players
"""


class Constants(BaseConstants):
    name_in_url = 'teams'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pref1 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )
    pref2 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )
    pref3 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )
    pref4 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )
    pref5 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )
    pref6 = models.IntegerField(
        min=0, max=100,
        verbose_name='Your preference weight:'
    )

class Preferences(Page):
    form_model = 'player'
    form_fields = ['pref1', 'pref2', 'pref3', 'pref4', 'pref5', 'pref6']

    def vars_for_template(player):
        pref = "pref"
        participant = player.participant
        order = [1,6,3,4,5,2]
        pic1 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='
        pic2 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='
        pic3 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='
        pic4 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='
        pic5 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='
        pic6 = 'iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAIAAAD+Tyo8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQESURBVHhe7dnRTp1AFEBR6f//MyWFGGOithZmZpu1HpTrkwE2Z+ay7fv+AjT9un4DQQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoawbd/365A7bNt2Hf3h9PIoAd/mTPft+Tz+4vTyKEvoe5ytypXBBPwU45cBYgG/22GuKfFP8jNkAj6qCNV7/DR+GaAR8NlDIonz/zxcn+FJgYAT00yxTBFo493KWSrwqrGEPqI9XZ+BP2LfQmsY3ooFDLzlbQeEmcAQJmAIE/CH3r2+ggUJ+EP7vmuYxQkYwgQMYQKGMAF/xjaYxQkYwgQMYQL+glU0KxMwhAn4a4YwyxIwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMDNt23Yd8S0ChjABM80xfvd9vz7wLQKGMAEzh/F7CwFDmICZwPi9i4AhTMCMZvzeSMAQJmAIEzCECZihbIDvJWAIEzCECRjCBMw4NsC3EzCECZhBjN8nCBjCBMwIxu9DBAxh0wI+HsnXET+d8fucOQGrF24xJ2DPY7iFPTDPsn5+lIAhbFrAx1PZTvjHM36fNnMCaxj+kyU0TzF+B5gcsCH8U6l3DBMYwgTM/YzfYQQMYfMDXn8bbJ78E6drJBP4a25HlrVEwOsPYViTCcydrJ8HWyVgQxi+Ya3nped31/n8dfkGWy4YDRe5arMstwc+7gNrafhLK36JpeEW43eiRb+F1nCFeuda9zWShten3unWDfigYfjc0gEfNLws43cFjWvgXlnH6/PUFVlBJgwNT3em6yospVSFG2gWZ35ZvbHmZhrJ2V5cdV163lg8TbqLs7GEsNVfIwGfEDCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ5iAIUzAECZgCBMwhAkYwgQMYQKGMAFDmIAhTMAQJmAIEzCECRjCBAxhAoYwAUOYgCFMwBAmYAgTMIQJGMIEDGEChjABQ9bLy29Rt/2kzgXPyAAAAABJRU5ErkJggg=='

        p1 = 1
        p2 = 2
        p3 = 3
        p4 = 4
        p5 = 5
        p6 = 6

        name1 = 'Regina'
        name2 = 'Amir'
        name3 = 'Nathalie'
        name4 = 'Ben'
        name5 = 'Rika'
        name6 = 'Kevin'

        self = 2
        return dict(
            order=order,
            p1 = p1, p2 = p2, p3=p3, p4=p4, p5=p5, p6=p6, self=self,
            pic1=pic1, pic2=pic2, pic3=pic3, pic4=pic4, pic5=pic5, pic6=pic6,
            name1=name1, name2=name2, name3=name3, name4=name4, name5=name5, name6=name6
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            order=[1,6,3,4,5,2]
        )


class Last(Page):
    pass

#page_sequence = [Instructions, Call1, WaitPage1, Call2, WaitPage2, Call3, WaitPage3, Last]
page_sequence = [Preferences]

from enum import Enum


class Library(Enum):
    """
    An enum to denote which type of API wrapper you are
    intending on using this with.
    CUSTOM will not set a library handler.
    You will need to set one yourself.
    """

    DPY = 1
    DISNAKE = 5
    NEXTCORD = 6
    PYCORD = 7
    CUSTOM = 8
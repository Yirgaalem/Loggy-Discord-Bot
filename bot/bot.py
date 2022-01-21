from discord.ext import commands

#Inherit from discord Bot class
class Bot(commands.Bot):
    def __init__(self, prefix: str):
        """Description: Constructor for discord Bot inherited from discord.ext.commands creates a bot which adds custom properties.
    

    Args:
        prefix (str): The prefix the which the bot recognizes to execute a named command
    """
        super().__init__(command_prefix=prefix)
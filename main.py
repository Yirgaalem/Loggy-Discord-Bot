from bot import bot
import os
from bot.keep_alive import keep_alive
     
keep_alive()
bot.run(os.environ.get("TOKEN"))


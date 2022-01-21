from .bot import Bot
import os
import yfinance as yf
import requests
from datetime import datetime
import logging
import discord
from logger.logger import initialize_logging
from threading import Thread
from zipfile import ZipFile
from producer import produce_logs
from consumer import consume_logs
from queue import Queue

initialize_logging()
bot = Bot('$')


@bot.event
async def on_ready():
      """Description: Event for bot when being initialized and starting up. Prints its name to the
    consolse.
      """
      print(f"Booting up: {bot.user}")



@bot.command(name="printLog")
async def print_log(ctx):
    """Description: Command to print logs into console on virtual machine. Called from discord when bot is active.
    Args:
      ctx (Context): Context in which the command is being invoked
    """
    for log in bot.log_stream.logs:
        print(log)
    await ctx.send(f"Log printed in console {datetime.now()}")


@bot.command(name="hello")
async def greeting(ctx):
  """Description: Command to reply to user and reply in discord chat with greeting.
  Args:
      ctx (Context): Context in which the command is being invoked
  """
  await ctx.send(f'Hello {ctx.author.display_name}')


@bot.command(name="enableLog")
async def enable_log(ctx):
  """Description: Command to enable logging from bot on virtual machine and store logs in a file.
  Args:
      ctx (Context): Context in which the command is being invoked
    """
  logging.disable(logging.NOTSET)
  await ctx.send(f"Logging enabled {datetime.now()}")


@bot.command(name="disableLog")
async def disable_log(ctx):
  """Description: Command called from discord, flushes bot log stream and disables logging.
  Args:
      ctx (Context): Context in which the command is being invoked
    """
  logging.disable(logging.CRITICAL)
  await ctx.send(f"Logging disabled {datetime.now()}")


@bot.command(name="file")
async def log_files(ctx):
  """Description: Command to send formatted log files to discord chat in a zip file format.
  Args:
      ctx (Context): Context in which the command is being invoked
    """
  with ZipFile("formatted_logs.zip", "w") as zip:
      folder_path = "formatted_logs"
      for _, _, files in os.walk(folder_path):
          for filename in files:
              zip.write("formatted_logs/" + filename)
      zip.close()
  await ctx.send(file=discord.File("formatted_logs.zip"))


@bot.command(name="smile")
async def smile(ctx):
  """Description: Command that is called that returns the image of the bot to the discord chat
  Args:
      ctx (Context): Context in which the command is being invoked
    """
  await ctx.send(file=discord.File("LoggySmile.png"))


def get_weather():
    """
    Currently only does weather for waterloo
    ---------------------------------------------
    Return: 
        msg - a string indicating the weather or if there was an error
    """
    key = os.environ.get("weather_key")
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q=Waterloo&units=metric&appid='
        + key)

    weather_report = {
        "complete": True
    }  # dictionary of weather info incase furthur processing is wanted
    msg = "An error has occured"

    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        weather_report["ctemp"] = main['temp']
        # getting high and low temps
        weather_report['max_temp'] = main['temp_max']
        weather_report['min_temp'] = main['temp_min']
        # getting the humidity
        weather_report["humidity"] = main['humidity']
        # weather description
        weather_report["description"] = data['weather'][0]['description']
        #format the msg that needs to be sent (could be updated to pythons new string formatting)
        msg = "Current temp: {}°C\nHigh: {}°C\nLow: {}°C\nHumidity: {}%\nDescription: {}\n".\
                format(weather_report["ctemp"],weather_report["max_temp"],weather_report["min_temp"],weather_report["humidity"],\
                    weather_report["description"])
    else:
        # showing the error message
        weather_report["complete"] = False
    return msg


@bot.command(name='weather')
async def on_message(ctx):
    """Description: Returns the weather for Waterloo to the discord chat

    Args:
        ctx (Context): Context in which the command is being invoked
    """
    await ctx.send(get_weather())

@bot.command(name="produce_consume")
async def produce_consume(ctx):
  """Description: Starts the producer-consumer architecture with the logs

    Args:
        ctx (Context): Context in which the command is being invoked
    """

  await ctx.send("Producing and consuming has started...")

  #Clearing old formatted log files
  for file in os.listdir("formatted_logs"):
    open("formatted_logs/"+file,'w').close()
    
  logging.disable(logging.CRITICAL)
  work = Queue()
  finished = Queue()

  #thread for producer
  #currently have it set up to work with a small file with one of each log types
  produce = Thread(target=produce_logs.produce_logs, args = (work, finished, "logging.txt"))

  #thread for consumer
  consume = Thread(target=consume_logs.consume_logs, args = (work, finished))   

  #start each thread
  produce.start()
  consume.start()
  
  produce.join()
  consume.join()
  # clears logging.txt file contents
  logging.getLogger().handlers[0].close()
  initialize_logging()
  
  print("Log file cleared")

  logging.disable(logging.NOTSET)
 

  # rows = []
  # with open('logging.txt', "r") as f:
  #       rows = f.readlines()[1:]
  # with open('logging.txt','w') as f:
  #       f.writelines(rows)
  await ctx.send("Finished")

  
  


# these two packages are used to create python dictionaries form strings
import ast
import json

"""
Overall Description:
  These classes are to be used once the proper log has been found and can be associated with the correct sub class, all unclassifiable logs can be created with the base class
Author:
  Brandon Parker - park3730
"""

# Base class ice cream juice
class Base_log_format:
  """
  Description:
    Used to create log objects from unclassified logs. Overall formatting done in this class is basic since the logs overall format is unknown and not implemented.

  Log type Example(s):
    DEBUG 2021-09-17 18:15:42,567 - http://api.openweathermap.org:80 "GET /data/2.5/weather?q=Waterloo .....  
    INFO 2021-09-17 19:31:13,218 - 172.18.0.1 - - [17/Sep/2021 19:31:13] "HEAD / HTTP/1.1" 200 -
  """

  formatted_msg = None
  csv_msg = None
  file_name = "formatted_other_logs_formatted.txt"
  csv_file_name = "csv_other_logs_csv.csv"

  def __init__(self, msg: str):
    self.msg = msg
    # call helper function to create the formatted messages
    self.format_msg()
    # creates the file names based on their class name except
    # for the base class
    if self.__class__.__name__ != "Base_log_format":
      self.file_name = "formatted_" + self.__class__.__name__ + ".txt"
      self.csv_file_name = "csv_" + self.__class__.__name__ + ".csv"

  def __str__(self):
    """
    Return:
      Formatted log as a string
    """
    return self.formatted_msg

  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """
    #print("Base Log formatting")

    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)
    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]
    # grab the remainder of the log
    info = remainder[6:]
    # create the formated message and CSV
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code} | Notes: {info}"
    self.csv_msg = f"{msg_type},{timestamp},{code},{info}"

  def write_to_file(self) -> None:
    """
    Description:
      Function to write the formatted message of the log object to the correct file
    -------------------------------------------
    Return:
      None
    """
    #print("Writing to file")
    # open file for appending
    file = open("formatted_logs/" + self.file_name,
                "a",
                encoding="utf-8")
    # write message to file
    file.write(self.formatted_msg + "\n")
    # close file
    file.close()

  def write_to_csv(self) -> None:
    """
    Description:
      Function to write the CSV message of the log object to the correct file
    -------------------------------------------
    Return:
      None
    """
    # open file for appending
    file = open("formatted_logs/" + self.csv_file_name,
                "a",
                encoding="utf-8")
    # write message to file
    file.write(self.csv_msg + "\n")
    # close file
    file.close()


# Dispatch Event Subclass
class dispatch_event_log(Base_log_format):
  """
  Description:
    Subclass of Base_log_format used to create log objects from disbatch events logs

  Log type Example(s):
    DEBUG 2021-09-17 18:09:19,721 - Dispatching event socket_raw_receive
    DEBUG 2021-09-17 18:09:19,722 - Dispatching event socket_response
  """
  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """
    #print("dispatch_event_log formatting")

    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)

    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]
    # grab the message
    event_msg = remainder[24:]

    # create formated messages
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code} | Dispatch Event: {event_msg}"
    self.csv_msg = f"{msg_type},{timestamp},{code},{event_msg}"


# Websocket Event subclass
class websocket_event_log(Base_log_format):
  """
  Description:
    Subclass of Base_log_format used to create log objects from websocket events logs

  Log type Example(s):
    DEBUG 2021-09-17 18:16:31,681 - For Shard ID None: WebSocket Event: {'t': None, 's': None, 'op': 11, 'd': None}
    DEBUG 2021-09-17 18:09:38,843 - For Shard ID None: WebSocket Event: {'t': 'MESSAGE_CREATE', 's': 33, 'op': 0, .....
  """
  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """
    #print("websocket_event_log Formatting")

    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)

    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]

    # gets the dictiionary style infomation from the string
    _, info = remainder[6:].split("{", 1)
    info = "{" + info

    # had to use the ast package to create dictionary form string as json needs the key to be in double quotes
    info_dict = ast.literal_eval(info)

    # create the parts of the formatted/CSV that will be the same for each log
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code}"
    self.csv_msg = f"{msg_type},{timestamp},{code}"

    # create the remaining part of the message based on log subtype
    if info_dict['t'] == 'MESSAGE_CREATE':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Author: {info_dict['d']['author']['username']} Message: {info_dict['d']['content']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['author']['username']},{info_dict['d']['content']}"

    elif info_dict['t'] == 'TYPING_START':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Author: {info_dict['d']['member']['user']['username']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['member']['user']['username']}"

    elif info_dict['t'] == 'CHANNEL_UPDATE':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Member ID: {info_dict['d']['permission_overwrites'][0]['id']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['permission_overwrites'][0]['id']}"

    elif info_dict['t'] == 'VOICE_STATE_UPDATE':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Member: {info_dict['d']['member']['user']['username']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['member']['user']['username']}"

    elif info_dict['t'] == 'MESSAGE_DELETE':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Channel ID: {info_dict['d']['channel_id']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['channel_id']}"

    elif info_dict['t'] == 'MESSAGE_UPDATE':
        self.formatted_msg += f" | Event Type: {info_dict['t']}"
        self.csv_msg += f",{info_dict['t']}"

    elif info_dict['t'] == 'CHANNEL_PINS_UPDATE':
        self.formatted_msg += f" | Event Type: {info_dict['t']} | Channel ID: {info_dict['d']['channel_id']}"
        self.csv_msg += f",{info_dict['t']},{info_dict['d']['channel_id']}"

    else:
        self.formatted_msg += f" | Event Type: miscellaneous"
        self.csv_msg += f",miscellaneous"


# POST subclass
class POST_log(Base_log_format):
  """
  Description:
    Subclass of Base_log_format used to create log objects from POST logs

  Log type Example(s):
    DEBUG 2021-09-17 18:10:50,049 - POST https://discord.com/api/v7/channels/887370975526653962/messages with {"content":"Current temp: 25.7\u00b0C\n .....
    DEBUG 2021-09-17 18:10:50,049 - POST https://discord.com/api/v7/channels/887370975526653962/messages has received {'id': '888487175790952478', 'type': 0, .....
  """
  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """

    #print("POST_log formatting")
    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)
    
    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]

    # gets the dictiionary style infomation from the string
    if "{" in remainder:
      _, remainder = remainder[6:].split("{", 1)
      remainder = "{" + remainder

      # Some logs had messages after the string dictionary so split the message
      data = remainder.split("} ", 1)

      # if the log had a following message the data would have a length greater than 1
      # which would mean the split function removed the "}" at the end which is
      # needed to create the dictionary. So the "}" is added back on if needed
      if len(data) > 1:
          data[0] += "}"

    else:
      data = []

    # create the parts of the formatted/CSV that will be the same for each log
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code}"
    self.csv_msg = f"{msg_type},{timestamp},{code}"
    
    if len(data) == 0:
      self.formatted_msg += f" | Notes: {remainder[11:]}"
      self.csv_msg += f",{remainder[11:]}"
      #print("1")
    elif len(data) == 1:
        #print("2")
        # had to use the ast package to create dictionary form string as json needs the key to be in double quotes
        info_dict = ast.literal_eval(data[0])

        # replace all the new line characters in the message with spaces so
        # when written to log file the format is more readable
        info_dict['content'] = info_dict['content'].replace("\n", " ")

        self.formatted_msg += f" | Author: {info_dict['author']['username']} | Message: {info_dict['content']} | Channel ID: {info_dict['channel_id']}"
        self.csv_msg += f",{info_dict['author']['username']},{info_dict['content']},{info_dict['channel_id']}"

    else:
        #print("3")
        # had to use json to create dictionary from string for characters in utc-16
        info_dict = json.loads(data[0])

        # replace all the new line characters in the message with spaces so
        # when written to log file the format is more readable
        info_dict['content'] = info_dict['content'].replace("\n", " ")

        self.formatted_msg += f" | Message: {info_dict['content']} | Notes: {data[1]}"
        self.csv_msg += f",{info_dict['content']},{data[1]}"


# Starting new HTTP connection subclass
class HTTP_connection_log(Base_log_format):
  """
  Description:
    Subclass of Base_log_format used to create log objects from HTTP Connection logs

  Log type Example(s):
    DEBUG 2021-09-17 18:15:42,142 - Starting new HTTP connection (1): api.openweathermap.org:80
    DEBUG 2021-09-17 18:10:49,631 - Starting new HTTP connection (1): api.openweathermap.org:80
  """
  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format
      and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """

    #print("HTTP_connection_log formatting")

    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)

    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]

    # splits the remainder of the information into 2 parts based on ":"
    info = remainder[6:].split(":")
    # Strips any white spaces
    info[1] = info[1].strip()

    # creating the formatted messages
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code} | Event: HTTP Connection | Website: {info[1]}"
    self.csv_msg = f"{msg_type},{timestamp},{code},HTTP Connection,{info[1]}"


# Keeping shard ID None websocket alive subclass
class websocket_alive_log(Base_log_format):
  """
  Description:
    Subclass of Base_log_format used to create log objects from websocket alive logs

  Log type Example(s):
    DEBUG 2021-09-17 18:10:20,378 - Keeping shard ID None websocket alive with sequence 34.
    DEBUG 2021-09-17 18:11:01,629 - Keeping shard ID None websocket alive with sequence 41.
  """
  def format_msg(self) -> None:
    """
    Description:
      Private Helper Method to convert the inital message into a more readable format
      and create a comma seperated version of the message.
    -------------------------------------------
    Return:
      None
    """

    #print("websocket_alive_log formatting")
    # splits data into the time stamp and remainder portion of the log
    type_and_timestamp, remainder = self.msg.split(',', 1)

    # grab just the timestamp
    timestamp = type_and_timestamp[-19:]
    # grab just the msg type
    msg_type = type_and_timestamp[:-20]
    # grab the code
    code = remainder[:3]

    # Creates the formatted messages
    self.formatted_msg = f"Type: {msg_type} | Timestamp: {timestamp} | Code: {code} | Notes: {remainder[6:]}"
    self.csv_msg = f"{msg_type},{timestamp},{code},{remainder[6:]}"

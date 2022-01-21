from queue import Queue
from log_format import log_format

def consume_logs(work: Queue, finished: Queue)->None:
  print("Consuming")
  while True:
    if not work.empty():
      line = work.get()
      #print(line+'\n')
      try:
        #Classify line here
        if "- Dispatching event" in line:
          log = log_format.dispatch_event_log(line)
        elif " - POST" in line:
          log = log_format.POST_log(line)
        elif " - For Shard ID None: WebSocket Event:" in line:
          log = log_format.websocket_event_log(line)
        elif " - Starting new HTTP connection" in line:
          log = log_format.HTTP_connection_log(line)
        elif " - Keeping shard ID None websocket alive with sequence" in line:
          log = log_format.websocket_alive_log(line)
        else:
          log = log_format.Base_log_format(line)
      except Exception as e:
        print(e)
        log = log_format.Base_log_format(line)
        
      
      #Might have to adjust line so that it removes uneccesary parts
      
      log.write_to_csv()
      log.write_to_file()
      

      
    else:
      finish = finished.get()
      if finish:
        break



#how to create a Dispatch Event
#dispatch = log_format.dispatch_event_log("DEBUG "

# Consumer
# def perform_work(work: Queue, finished: Queue) -> None:
#     """Consumes the data given from the producer function

#     Args:
#         work (Queue): Filled with random numbers to be assigned
#         finished (Queue): Boolean as to whether the work if finished or not
#     """
#     counter = 0
#     while True:
#         if not work.empty():
#             v = work.get()
#             display(f"Consuming {counter}: {v}")
#             counter += 1
#         else:
#             q = finished.get()
#             if q:
#                 break
#             display("finished")

#--------------------------------------------------------------

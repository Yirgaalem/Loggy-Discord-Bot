from queue import Queue
def produce_logs(work: Queue, finished: Queue,filename:str)->None:
  print("Producing")
  with open(filename,"r") as file:
    finished.put(False)
    for line in file:
      work.put(line.strip())
      print(f"Producing: {line}")
    finished.put(True)

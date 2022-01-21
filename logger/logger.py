import logging
def initialize_logging()->None:
  file_handler = logging.FileHandler(filename="logging.txt",encoding="utf-8",mode='w')
  logging.basicConfig(
        handlers=[file_handler],
        format="%(levelname)s %(asctime)s - %(message)s",level = logging.DEBUG)
  logging.disable(logging.CRITICAL)
  return
  

  
import logging
from logging.handlers import RotatingFileHandler

FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('mirrulations')
handler = RotatingFileHandler('mirrulations.log', mode='w', backupCount=1)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.handlers[0].doRollover()

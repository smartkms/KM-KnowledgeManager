import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(name)s: %(message)s")

def getLogger(name : str) -> logging.Logger :
    return logging.getLogger(name=name)
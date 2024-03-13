from src.implementation import StartStopPostgres
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


if __name__ == '__main__':
    logger.info("Starting...")
    StartStopPostgres().run()
    logger.info("Finished!")
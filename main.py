import os
from ingestion.service.ingestion_service import IngestionService
from app.service.sp_budget_service import SPBudgetService
from config.logger import Logger


logger_obj = Logger()
logger = logger_obj.get_log()


def run_ingestion():
    """
    Calls ingestion pipeline.
    """

    logger.info(f'''{os.getenv("SOURCE")} ingestion: Starting....''')

    ingestion_service = IngestionService(logger)
    ingestion_service.execute(source=os.getenv("SOURCE"))

    logger.info(f'''{os.getenv("SOURCE")} ingestion: Done.''')


def run_app():
    """
    Calls app pipeline.
    """

    logger.info(f'''{os.getenv("SOURCE")} app: Starting....''')

    sp_budget_service = SPBudgetService(logger)
    sp_budget_service.execute()

    logger.info(f'''{os.getenv("SOURCE")} app: Done.''')


if __name__ == '__main__':
    if os.getenv("ENGINE") == 'ingestion':
        run_ingestion()
    elif os.getenv("ENGINE") == 'app':
        run_app()
    else:
        logger.error(f'''Invalid engine.''')

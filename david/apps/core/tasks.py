import logging

from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task(name="debug_logger")
def debug_logger(caller_name: str):
    logger.info(f"Debug task is called by {caller_name}")

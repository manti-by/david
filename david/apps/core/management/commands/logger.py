import logging

from command_log.management.commands import LoggedCommand


logger = logging.getLogger(__name__)


class Command(LoggedCommand):
    help = description = "Void logger management command."

    def handle(self, *args, **options):
        logger.info("Management command is called")

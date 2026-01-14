import factory
import factory.fuzzy
from factory import DictFactory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import User
from django.utils import timezone


DEFAULT_USER_PASSWORD = "pa55word"  # noqa

# Valid Python logging levels
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", DEFAULT_USER_PASSWORD)

    class Meta:
        model = User


class DjangoAdminUserFactory(UserFactory):
    is_superuser = True


class LogDataFactory(DictFactory):
    name = factory.LazyFunction(lambda: "david.apps.core")  # Valid logger name format
    msg = factory.Faker("sentence")
    filename = factory.Faker("word")
    levelname = factory.fuzzy.FuzzyChoice(LOG_LEVELS)  # Valid log level
    asctime = factory.LazyFunction(lambda: timezone.now())  # Current time (not future)

from django.apps import AppConfig
from django.db.models.signals import pre_save


class PollsConfig(AppConfig):
    name = 'polls'

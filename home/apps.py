from django.apps import AppConfig
from django.template.context import BaseContext


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if getattr(BaseContext.__copy__, '__name__', '') == 'safe_copy':
            return

        def safe_copy(self):
            duplicate = object.__new__(self.__class__)
            duplicate.__dict__ = self.__dict__.copy()
            duplicate.dicts = self.dicts[:]
            return duplicate

        BaseContext.__copy__ = safe_copy

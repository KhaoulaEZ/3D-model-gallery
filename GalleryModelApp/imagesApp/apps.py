from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class ImagesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imagesApp'

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'

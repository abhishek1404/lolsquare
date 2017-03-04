from django.apps import AppConfig


class MetastoreConfig(AppConfig):
    name = 'metastore'
    verbose_name = 'Metastore'

    def ready(self):
        super(MetastoreConfig, self).ready()


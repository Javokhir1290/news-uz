from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'


    def ready(self):
        from .signals import  comment_signal, news_signal





 # create_signal, delete_signal, comment_delete_signal
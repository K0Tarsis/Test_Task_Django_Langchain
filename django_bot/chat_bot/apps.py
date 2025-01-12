from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ChatBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_bot'

    def ready(self):
        post_migrate.connect(run_setup_tasks, sender=self)

def run_setup_tasks(sender, **kwargs):
    from chat_bot.task_setup import setup_periodic_tasks
    setup_periodic_tasks()

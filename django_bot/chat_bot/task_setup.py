from django_celery_beat.models import PeriodicTask, IntervalSchedule


def setup_periodic_tasks():
    print("Setting up periodic tasks...")

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,
    )

    PeriodicTask.objects.update_or_create(
        name="Scheduled Scraping Task",
        defaults={
            'task': 'chat_bot.tasks.scrape_homes',
            'interval': schedule,
            'args': '{"all_pages":false}'
        }
    )
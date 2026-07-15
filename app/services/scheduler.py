from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.news_jobs import send_ai_news

scheduler = BackgroundScheduler(
    timezone="Africa/Lagos"
)


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        send_ai_news,
        trigger="cron",
        hour=8,
        minute=0,
        args=[
            "+2348065440075, 08033507714"
        ],
        id="daily_ai_news",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=300,
    )

    scheduler.start()

    print("Scheduler started.")
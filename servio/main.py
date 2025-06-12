from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from .db.sqlite import sqlite_engine
from .models.sqlite_models import SQLiteBase
from .routes import firebird_routes, sqlite_routes
from .tasks import scheduled_job

app = FastAPI()
scheduler = BackgroundScheduler()

scheduler.add_job(scheduled_job, 'cron', hour=7, minute=50)


@app.on_event("startup")
def start_scheduler():
    SQLiteBase.metadata.create_all(bind=sqlite_engine)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


app.include_router(firebird_routes.router)
app.include_router(sqlite_routes.router)

from application.celery import celery
from application.worker import ingest_worker, remote_worker, sync_worker
from datetime import timedelta


@celery.task(bind=True)
def ingest(self, directory, formats, name_job, filename, user):
    resp = ingest_worker(self, directory, formats, name_job, filename, user)
    return resp


@celery.task(bind=True)
def ingest_remote(self, source_data, job_name, user, loader):
    resp = remote_worker(self, source_data, job_name, user, loader)
    return resp


@celery.task(bind=True)
def schedule_syncs(self):
    resp = sync_worker(self)
    return resp


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    interval_days = 30
    sender.add_periodic_task(
        timedelta(days=interval_days),
        schedule_syncs.s(),
    )

from celery import Celery

# from ..app import app

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

celery = Celery()


def ready_tasks_monitor(app):
    state = app.events.State()

    def announce_ready_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK READY: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-succeeded': announce_ready_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

# ready_tasks_monitor(celery)
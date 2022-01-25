from celery import shared_task

@shared_task(name="say_hello")
def hello(x):
    return "Hello " + str(x)
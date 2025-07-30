from time import sleep
from celery import shared_task


@shared_task
def notify_customer(message: str):
    print("Sending multiple emails...")
    print(message)
    sleep(10)
    print("Emails sent successfully!")

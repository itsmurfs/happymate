from __future__ import absolute_import

from celery import shared_task

from happyfridge.models import ShoppingRun


@shared_task
def run_expiration_check():
    result = -1
    for shopping_run in ShoppingRun.objects.filter(activated=True):
        if shopping_run.expire_time() <= 0:
            result = shopping_run.close()

    return result
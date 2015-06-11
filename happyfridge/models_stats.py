from django.db import models


def create_shopping_run_deleted(shopping_run):
    """
    """

    sr_deleted = ShoppingRunDeleted()

    sr_deleted.days = shopping_run.days
    sr_deleted.run_number = shopping_run.run_number
    sr_deleted.creation_date = shopping_run.creation_date
    sr_deleted.activation_date = shopping_run.activation_date
    sr_deleted.hearthstone = shopping_run.inn.hearthstone

    sr_deleted.save()

    return sr_deleted


def create_item_deleted(item, inn):

    item_deleted = ItemDeleted()

    sr_deleted = ShoppingRunDeleted.objects.filter(hearthstone=inn.hearthstone)
    sr_deleted = sr_deleted.order_by('deleted_date').last()

    item_deleted.name = item.name
    item_deleted.status = item.status
    item_deleted.category_name = item.category.name
    item_deleted.req_who_username = item.req_who.user.username
    item_deleted.check_who_username = item.check_who.user.username if item.check_who else None
    item_deleted.shopping_run = sr_deleted
    item_deleted.quantity = item.quantity

    item_deleted.save()

    return item


class ItemDeleted(models.Model):
    """

    """
    name = models.CharField(max_length=32)
    status = models.CharField(max_length=4)
    category_name = models.CharField(max_length=10)
    #item's creator
    req_who_username = models.CharField(max_length=80)
    #item's "processor" or buyer
    check_who_username = models.CharField(max_length=80, null=True)
    shopping_run = models.ForeignKey("ShoppingRunDeleted", related_name='item_pool')
    #quantity must be (^\d+ \w+$)
    quantity = models.CharField(max_length=105)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class ShoppingRunDeleted(models.Model):
    """
    """

    days = models.IntegerField(max_length=100)
    run_number = models.IntegerField(max_length=52, default=1)
    creation_date = models.DateField()
    activation_date = models.DateField()
    hearthstone = models.CharField(max_length=256)

    deleted_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'shopping run #{0}, total days {1}'.format(self.run_number, self.days)
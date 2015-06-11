import datetime

from django.core.exceptions import PermissionDenied

from happyfridge import models_stats
from happyfridge.models_stats import *


def get_processing_items(roommate):
    """
    this methods returns  user processing items:
        SELECT * from  item WHERE item.check_who == roomate AND item.status == "PROC"
    """
    return roommate.item_spotted.filter(status=Item.PROCESSING_CODE)

def get_shopping_run(user):
    """

    """
    try:
        sr = user.roommate.inn.shoppingrun
    except ShoppingRun.DoesNotExist:
        sr = None

    return sr


class Category(models.Model):
    """
    """
    name = models.CharField(max_length=10)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_top_items(self):
        items = self.item_set.order_by("-priority")[:3]
        return items


class Item(models.Model):
    """

    """
    CHECKED_CODE = u'CHEK'
    PROCESSING_CODE = u'PROC'
    UNCHECKED_CODE = u'UCHK'

    STATUS_CHOICES = ((CHECKED_CODE, u'checked'),
                      (PROCESSING_CODE, u'processing'),
                      (UNCHECKED_CODE, u'unchecked'))

    PRIORITY_VERY_HIGH_CODE = 5
    PRIORITY_HIGH_CODE = 4
    PRIORITY_NORMAL_CODE = 3
    PRIORITY_LOW_CODE = 2
    PRIORITY_VERY_LOW_CODE = 1

    PRIORITY_CHOICES = ((PRIORITY_VERY_HIGH_CODE, 'very high'),
                        (PRIORITY_HIGH_CODE, 'high'),
                        (PRIORITY_NORMAL_CODE, 'normal'),
                        (PRIORITY_LOW_CODE, 'low'),
                        (PRIORITY_VERY_LOW_CODE, 'very low'))

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default=UNCHECKED_CODE)
    category = models.ForeignKey("Category")
    #item's creator
    req_who = models.ForeignKey("happymate.Roommate", related_name='item_requested')
    #item's "processor" or buyer
    check_who = models.ForeignKey("happymate.Roommate", related_name='item_spotted', blank=True, null=True)
    shopping_run = models.ForeignKey("ShoppingRun", related_name='item_pool')
    #quantity must be (^\d+ \w+$)
    QUANTITY_REGEX = r'^\d+ \w+$'
    quantity = models.CharField(max_length=105)
    priority = models.IntegerField(max_length=2, choices=PRIORITY_CHOICES, default=3)

    #TODO rename roommate in roommate_instance
    def process(self, roommate):
        """
        Set the item status in progress.
        The item must be in status unchecked
        """
        if self.status == Item.UNCHECKED_CODE:
            self.status = Item.PROCESSING_CODE
            self.check_who = roommate
        else:
            raise PermissionDenied

    def check(self, roommate_instance):
        """
        Set the item status in check
        The item must be in status processing and the roommate which request the
        action must be the check_who user
        """
        if self.status == Item.PROCESSING_CODE and self.check_who == roommate_instance:
            self.status = Item.CHECKED_CODE
        else:
            raise PermissionDenied

    def uncheck(self, roommate_instance):
        """
        Set the item status in unchecked
        The item must be in status processing and the roommate which request the
        action must be the check_who user
        """
        if self.status == Item.PROCESSING_CODE and self.check_who == roommate_instance:
            self.status = Item.UNCHECKED_CODE
            self.check_who = None
        else:
            raise PermissionDenied

    def __unicode__(self):
        return u'{0}'.format(self.name)


class ShoppingRun(models.Model):
    """
    """
    days = models.IntegerField(max_length=100)
    run_number = models.IntegerField(max_length=52, default=1)
    creation_date = models.DateField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    activation_date = models.DateField(null=True)
    inn = models.OneToOneField("happymate.Inn")

    def __unicode__(self):
        return u'shopping run #{0}, total days {1}'.format(self.run_number, self.days)

    #TODO is_expired

    def expire_time(self):

        if not self.activation_date:
            #the shopping run isn't activated yet.
            #so it can't be expired
            return 1

        today = datetime.date.today()
        expires_in = today - self.activation_date

        return self.days - expires_in.days

    def close(self):
        """
        Step #1: takes get_innall checked items and Delete them all
        Step #2: creates a new shopping run with the same information of the instance
        updated with new timestamp and expiration date
        Step #3: set activated of this shopping_run to false
        Step #4: migrate all roommate from this to the new shopping run

        !!!NOTE!!!
        "Delete" means that when the Item instance is deleted, all his information will be stored inside the
        ItemDeletmodels.ForeignKey("Category")ed table on database.
        """

        #TODO protection check expire time

        #TODO comments
        models_stats.create_shopping_run_deleted(self)

        new_shopping_run = ShoppingRun()
        new_shopping_run.activated = False
        new_shopping_run.days = self.days
        new_shopping_run.run_number = self.run_number+1
        new_shopping_run.inn = self.inn

        item_pending = []

        for item in self.item_pool.all():
            if item.status == Item.CHECKED_CODE:
                create_item_deleted(item, self.inn)
                item.delete()
            else:
                item_pending.append(item)

        self.delete()
        new_shopping_run.save()

        for item in item_pending:
            item.shopping_run = new_shopping_run
            item.save()

        return 0
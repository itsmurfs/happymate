from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from happyfridge.models import Item, ShoppingRun, Category
from happyfridge.models_stats import ShoppingRunDeleted, ItemDeleted
from happymate.models import Roommate
from happyfridge.tasks import run_expiration_check


class CloseShoppingRunTests(TestCase):
    """

    """

    #TODO fix for item with status unchk
    def create_item(self, name, cat, r1, sr, status):
        Item.objects.create(name=name + status[1],
                                   description=name,
                                   status=status[0],
                                   req_who=r1,
                                   check_who=r1,
                                   category=cat,
                                   shopping_run=sr)

    def create_shopping_run(self, shared_key, u1, u2):
        sr = ShoppingRun.objects.create(days=7, shared_key=shared_key, activated=True, activation_date=datetime.now())
        r1 = Roommate.objects.create(user=u1, profile_picture="", shopping_run=sr)
        r2 = Roommate.objects.create(user=u2, profile_picture="", shopping_run=sr)
        cat = Category.objects.create(name="testCategory", slug="t")
        for (counter, status) in enumerate(Item.STATUS_CHOICES):
            self.create_item("test" + str(counter), cat, r1, sr, status)

    def get_users(self, prefix):
        u1 = User.objects.get(username=prefix+"1")
        u2 = User.objects.get(username=prefix+"2")
        return u1, u2

    def setUp(self):

        u1, u2 = self.get_users("user1")
        self.create_shopping_run("0a0a0a0a0a0", u1, u2)

        u1, u2 = self.get_users("user2")
        self.create_shopping_run("shared2", u1, u2)

    def tearDown(self):
        ShoppingRun.objects.all().delete()
        Roommate.objects.all().delete()
        Category.objects.all().delete()
        Item.objects.all().delete()
        ItemDeleted.objects.all().delete()
        ShoppingRunDeleted.objects.all().delete()

    def assert_shopping_run_after_close(self, roommate_count, shared_key, sr_id_old, item_to_delete_count):
        sr_set = ShoppingRun.objects.filter(shared_key=shared_key)
        self.assertEqual(sr_set.count(), 2)
        ##################
        # Assert new shopping run
        ##################
        old_sr = sr_set.first() if sr_set.first().id == sr_id_old else sr_set[1]
        new_sr = sr_set.first() if sr_set.first().id != sr_id_old else sr_set[1]

        try:
            sr_deleted = ShoppingRunDeleted.objects.get(shared_key=shared_key)
        except ObjectDoesNotExist:
            self.fail("Shopping run deleted not found")

        item_deleted_count = sr_deleted.item_pool.all().count()

        self.assertEqual(item_to_delete_count, item_deleted_count)

        self.assertEqual(old_sr.item_pool.filter(status=Item.CHECKED_CODE).count(), 0)

        self.assertEqual(new_sr.inn.id, old_sr.inn.id)
        self.assertEqual(new_sr.run_number, old_sr.run_number + 1)
        self.assertEqual(new_sr.days, old_sr.days)
        self.assertEqual(old_sr.roommate_set.count(), 0)
        self.assertEqual(new_sr.roommate_set.count(), roommate_count)
        self.assertFalse(new_sr.activated)
        self.assertFalse(old_sr.activated)

    def test_shopping_run_close(self):
        sr = ShoppingRun.objects.get(shared_key="0a0a0a0a0a0")
        item_to_delete_count = sr.item_pool.filter(status=Item.CHECKED_CODE).count()
        roommate_count = sr.roommate_set.count()
        sr.close()

        self.assert_shopping_run_after_close(roommate_count, "0a0a0a0a0a0", sr.id, item_to_delete_count)

    def test_shopping_run_task(self):

        sr = ShoppingRun.objects.get(shared_key="0a0a0a0a0a0")
        roommate_count = sr.roommate_set.count()
        item_to_delete_count = sr.item_pool.filter(status=Item.CHECKED_CODE).count()

        def mock_expire_time(self):
            if self.id == sr.id:
                return 0
            else:
                return 1

        ShoppingRun.expire_time = mock_expire_time

        #Task to test
        run_expiration_check()

        #Only one sr should be closed
        self.assert_shopping_run_after_close(roommate_count, "0a0a0a0a0a0", sr.id, item_to_delete_count)

    @classmethod
    def create_user(cls, prefix):
        User.objects.create(username=prefix+'1')
        User.objects.create(username=prefix+'2')

    @classmethod
    def setUpClass(cls):
        cls.create_user("user1")
        cls.create_user("user2")

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
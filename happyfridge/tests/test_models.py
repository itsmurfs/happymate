from django.contrib.auth.models import User
from django.test import TestCase

from happyfridge import models


class CategoryTests (TestCase):
    """

    """
    def test_get_top_items(self):
        cat = models.Category(name="test")
        cat.save()

        user = User.objects.create(username="testuser")
        user.save()

        roomate = models.Roommate.objects.create(user=user)
        roomate.save()

        for i in range(0):
            item = models.Item(name="test"+str(i),
                               description="description"+str(i),
                               req_who=roomate,
                               check_who=roomate,
                               priority=3,
                               category=cat)
            item.save()

        item = models.Item(name="test",
                           description="description",
                           req_who=roomate,
                           check_who=roomate,
                           priority=5,
                           category=cat)
        item.save()

        topitem = cat.get_top_items()

        self.assertEqual(topitem[0].name, item.name)

        cat.delete()
        user.delete()


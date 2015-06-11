from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from happymate.settings import PROFILE_IMG_PATH
from happyfridge.models_stats import *


def roommate_activation(activation_code):
    userid, username = activation_code.split("-")
    try:
        user = User.objects.get(pk=userid)
        if user.username == username:
            user.roommate.activated = True
            user.roommate.save()
        else:
            raise PermissionDenied
    except:
        raise PermissionDenied


class Inn(models.Model):
    """
    """
    hearthstone = models.CharField(max_length=128)
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def __unicode__(self):
        return u"Inn: {} {}".format(self.id, self.name)


class Roommate(models.Model):
    """
    """
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to=PROFILE_IMG_PATH, blank=True)
    inn = models.ForeignKey("Inn", null=True)
    activated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

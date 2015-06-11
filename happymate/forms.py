from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput

from happymate.models import Roommate, Inn


def get_config_inn_form(roommate):
    """
    :param roommate:
    :return:
    """
    class ConfigInnForm(forms.ModelForm):
        """

        """
        class Meta:
            model = Inn
            fields = ['name', 'password']
            widgets = {"password": PasswordInput}

        def save(self, commit=True):
            inn = super(ConfigInnForm, self).save(commit=False)
            inn.set_password(self.cleaned_data['password'])
            #TODO Create Hearthstone
            inn.save()

            roommate.inn = inn
            roommate.save()

            return inn

    return ConfigInnForm


def get_user_create_form():

    class UserCreateForm(forms.ModelForm):

        class Meta:
            model = User
            #TODO discover how to send emails
            fields = ['username', 'password', 'first_name', 'last_name', 'email']
            widgets = {"password": PasswordInput}

    return UserCreateForm


def get_roommate_create_form():

    class RoommateCreateForm(forms.ModelForm):

        class Meta:
            model = Roommate
            fields = ['profile_picture']

    return RoommateCreateForm


def get_roommate_edit_profile_form(roommate):
    """

    :return:
    """
    class RoommateEditForm(forms.ModelForm):
        class Meta:
            model = Roommate
            fields = ['profile_picture']

    RoommateInnChangeForm = get_config_inn_form(roommate)

    class UserEditForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']

    class UserPasswordChangeForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['password']
            widgest = {"password": PasswordInput}

    return RoommateEditForm, RoommateInnChangeForm, UserEditForm, UserPasswordChangeForm
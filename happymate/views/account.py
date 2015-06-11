from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from happymate import settings
from happymate.forms import get_config_inn_form, get_user_create_form, get_roommate_create_form, \
    get_roommate_edit_profile_form
from happymate.models import roommate_activation, Inn


def login(request, *args, **kwargs):
    """

    """
    httpResponse = django_login(request, *args, **kwargs)

    #TODO move the following checks into a middleware
    if request.user.is_authenticated():
        if not request.user.roommate.activated:
            return HttpResponse("You account is not activated yet. Please click on the activation link")
        if not request.user.roommate.inn:
            return HttpResponseRedirect(reverse("config_inn"))
    return httpResponse


def register(request):

    UserCreateForm = get_user_create_form()
    RoommateCreateForm = get_roommate_create_form()

    if request.POST:
        user_form = UserCreateForm(request.POST)
        roommate_form = RoommateCreateForm(request.POST)

        if user_form.is_valid() and roommate_form.is_valid():
            user_form.instance.set_password(user_form.cleaned_data['password'])
            u = user_form.save()
            r = roommate_form.instance
            r.user = u
            roommate_form.save()
            send_activation_mail(u)

            return HttpResponse("A mail has sent to your address with the activation link. Thank you.")

    else:
        user_form = UserCreateForm()
        roommate_form = RoommateCreateForm()

    return render(request, 'happymate/account_register.html', {'user_form': user_form,
                                                               'roommate_form': roommate_form})


def activate(request):
    if request.method == "GET":
        if "activation_code" in request.GET:
            activation_code = request.GET["activation_code"]
            roommate_activation(activation_code)
            return HttpResponseRedirect(reverse("home"))
    raise PermissionDenied


def send_activation_mail(user):
    activation_code = "{}-{}".format(user.id, user.username)
    link = "{}{}?activation_code={}".format(settings.ACCOUNT_LINK_BASE_URL,
                                            reverse("activate"),
                                            activation_code)

    body = "to start using happymate just click on the link below :\n {}".format(link)

    if not settings.DEBUG:
        send_mail('happymate staff',
                  body,
                  settings.EMAIL_HOST_USER,
                  [user.email],
                  fail_silently=False)
    else:
        print(body)



@login_required
def config_inn(request):
    ConfigInnForm = get_config_inn_form(request.user.roommate)
    if request.POST:
        if 'create_inn' in request.POST and request.POST['create_inn']:
            inn_form = ConfigInnForm(request.POST)
            if inn_form.is_valid():
                inn_form.save()
                return HttpResponseRedirect(reverse("home"))
        else:
            inn = get_object_or_404(Inn, name=request.POST['name'])
            if inn.check_password(request.POST['password']):
                roommate = request.user.roommate
                roommate.inn = inn
                roommate.save()
                return HttpResponseRedirect(reverse("home"))
            else:
                raise PermissionDenied

    else:
        inn_form = ConfigInnForm()

    return render(request, "happymate/account_config_inn.html", {"inn_form": inn_form})


@login_required()
def edit_profile(request):

    roommate = request.user.roommate
    RoomateEditForm, InnChangeForm, UserEditForm, UserPasswordChangeForm = get_roommate_edit_profile_form(roommate)
    roommate_edit_form = RoomateEditForm(instance=roommate)
    inn_change_form = InnChangeForm()
    user_edit_form = UserEditForm(instance=request.user)
    user_password_change_form = UserPasswordChangeForm(request.user)

    if request.POST:
        pass
    else:
        roommate_edit_form = RoomateEditForm(instance=roommate)
        inn_change_form = InnChangeForm()
        user_edit_form = UserEditForm(instance=request.user)
        user_password_change_form = UserPasswordChangeForm(instance=request.user)

    return render(request, "happymate/account_edit_profile.html", {"roommate_edit_form": roommate_edit_form,
                                                                   "inn_change_form": inn_change_form,
                                                                   "user_edit_form": user_edit_form,
                                                                   "user_password_change_form": user_password_change_form})
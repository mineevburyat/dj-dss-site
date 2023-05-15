# from catalog.models import Basket
# from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from .forms import FormAuth, FormChangeProfile, FormRegister
from .models import User, VerifideUser
from common.mixins import TitleMixin

from django.utils.timezone import now


class AuthView(TitleMixin, LoginView):
    template_name = 'user/login.html'
    authentication_form = FormAuth
    next_page = '/'
    title = "ДСС: Аутентификация"


class RegisterUserView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    template_name = 'user/register.html'
    form_class = FormRegister
    success_url = '/user/login'
    success_message = 'успешно зарегестрирован'
    title = "ДСС: Регистрация"


class ProfileEditView(TitleMixin, UpdateView):
    model = User
    form_class = FormChangeProfile
    template_name = 'user/profile.html'
    success_message = 'профиль изменен'
    title = "ДСС: Профиль"

    def get_success_url(self) -> str:
        return reverse_lazy('user:profile', kwargs={'pk': self.object.id})


class MyLogoutView(LogoutView):
    pass


class VerificationView(TitleMixin, TemplateView):
    template_name = 'user/email_verification.html'
    title = 'ДСС: верефицирован'

    # TODO send message error on index page
    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', '')
        uuid_str = kwargs.get('code', '')
        # try:
        #     code = uuid.UUID(uuid_str)
        # except ValueError:
        #     # return HttpResponseNotFound('uuid is not valide')
        #     return HttpResponseRedirect(reverse('index'))
        # ставь в urls uuid и проверять не придется, не найдет на этапе маршрутизации
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.last()
        record = VerifideUser.objects.filter(user=user, code=uuid_str).last()
        if record:
            if record.expiration > now():
                user.is_verified_email = True
                user.save()
                # record.delete()
                return super().get(request, *args, **kwargs)
            else:
                print('time out')
        else:
            print('uuid not found')
        return HttpResponseRedirect(reverse('index'))

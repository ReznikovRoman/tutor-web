from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

from . import models as account_models
from . import forms as account_forms


##################################################################################################################


class SignUp(generic.CreateView):
    form_class = account_forms.CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = ''  # TODO: 'account' templates

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(SignUp, self).get(request, *args, **kwargs)


# TODO: 'account' views







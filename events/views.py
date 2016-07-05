import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
import django.forms
from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

# from events.models import Status
from . import forms
from . import models


# TODO - replace inheritance from LoggedInMixin to an existing
class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)

    pass


class LoginView(FormView):
    page_title = "Login"
    template_name = "login.html"
    form_class = forms.LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('events:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None:
            if user.is_active:
                login(self.request, user)

                if self.request.GET.get('from'):
                    return redirect(
                        self.request.GET['from'])  # SECURITY: check path
            else:
                form.add_error(None, "User isn't active anymore - plz contact admin")
                return self.form_invalid(form)
        else:
            form.add_error(None, "username doesn't exist")
            return self.form_invalid(form)
        return redirect('events:user_list')


class CreateUserView(CreateView):
    page_title = "Signup"
    model = models.Profile
    form_class = forms.SignupForm

    success_url = reverse_lazy('events:user_list')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         return redirect('events:user_list')
    #     return super().dispatch(request, *args, **kwargs)

    # def get_initial(self):
    #     d = super().get_initial()
    #     d['date'] = datetime.date.today()
    #     return d

    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data.pop('password_confirm'):
            form.add_error(None, "Passwords do not match")
            return self.form_invalid(form)

        is_matchmaker, is_single = form.cleaned_data.pop('is_matchmaker'), form.cleaned_data.pop('is_single')
        if is_matchmaker == is_single:
            form.add_error(None, "User must be a matchmaker or writer (not both).")
            return self.form_invalid(form)
        gender = form.cleaned_data.pop('gender')
        status = form.cleaned_data.pop('status')
        is_cohen = form.cleaned_data.pop('is_cohen')

        # Add new user instance
        try:
            user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(**form.cleaned_data)
        except IntegrityError:
            form.add_error(None, "The username is already exist, please try another one.")
            return self.form_invalid(form)

        # Add new user to Profile
        pu = models.Profile(user=user, )
        pu.gender = gender
        pu.status = status
        pu.is_cohen = is_cohen
        pu.is_single = is_single
        pu.is_matchmaker = is_matchmaker
        pu.full_clean()
        pu.save()

        # Login
        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                form.add_error(None, "Disabled account")
                return self.form_invalid(form)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('events:user_list')

        resp = super().form_valid(form)
        messages.success(self.request, "User created successfully.")
        return resp


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ListUserView(LoggedInMixin, ListView):
    page_title = "Users List"
    model = models.Profile
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_active and self.request.user.profile.is_single:
            return redirect("events:home")
        return super().dispatch(request, *args, **kwargs)


class CreateEventView(LoggedInMixin, CreateView):
    page_title = "Event Adding - Form"
    model = models.Event
    fields = (
        'title',
        'description',
        # 'link',
        'date',
        'singles_num',
    )

    success_url = reverse_lazy('events:user_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.is_single:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    # def get_initial(self):
    #     d = super().get_initial()
    #     d['date'] = datetime.date.today()
    #     return d

    def form_valid(self, form):
        pu = models.Profile.objects.get(
            user_id=self.request.user.pk)
        form.instance.owner = models.Profile.objects.get(
            user=pu.pk)
        resp = super().form_valid(form)
        # messages.SUCCESS(self.request, "event added successfully.") #TODO
        return resp


class ListEventView(LoggedInMixin, ListView):
    page_title = "event list"
    model = models.Event
    paginate_by = 5

    def get_queryset(self):
        try:
            if self.request.user.profile.is_matchmaker:
                return super().get_queryset().filter(
                    owner=models.Profile.objects.get(
                        user=self.request.user.pk))
        except ObjectDoesNotExist:
            print("This user must be a Matchmaker or Single.")


class EventDetailView(LoggedInMixin, DetailView):
    page_title = "event Details"
    model = models.Event

    def dispatch(self, request, *args, **kwargs):
        self.request.session['event_id'] = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

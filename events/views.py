import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from events.models import Status
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


class SignupView(FormView):
    page_title = "Signup"
    template_name = "signup.html"
    form_class = forms.SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('events:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data.pop('password_recheck'):
            form.add_error(None, "Passwords do not match")
            return self.form_invalid(form)

        is_matchmaker, is_single = form.cleaned_data.pop('is_matchmaker'), form.cleaned_data.pop('is_single')
        if is_matchmaker == is_single:
            form.add_error(None, "User must be a matchmaker or writer (not both).")
            return self.form_invalid(form)

        # Add new user instance
        user = User.objects.create_user(**form.cleaned_data)
        # user = authenticate(**form.cleaned_data)

        # Add new user to Profile
        pu = models.Profile(user=user, )
        pu.gender = form.cleaned_data['gender']
        pu.status = Status.SINGLE if form.cleaned_data['status'] == 'single' else Status.DIVORCEE
        pu.is_cohen = form.cleaned_data['is_cohen']
        pu.is_single = form.cleaned_data['is_single']
        pu.is_matchmaker = form.cleaned_data['is_matchmaker']
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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ListUserView(LoggedInMixin, ListView):
    page_title = "users list"
    model = models.Profile
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_active and self.request.user.profile.is_single:
            return redirect("events:home")
        return super().dispatch(request, *args, **kwargs)


class CreateEventView(LoggedInMixin, CreateView):
    page_title = "event Adding - Form"
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
        # if self.request.user.is_single:
        # return super().get_queryset().all()
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

# class CreateReplyView(LoggedInMixin, CreateView):
#     page_title = "Reply to event "
#     model = models.Reply
#     fields = (
#         'reply_text',
#     )
#
#     success_url = reverse_lazy('events:user_list')
#
#     def form_valid(self, form):
#         pu = models.Profile.objects.get(
#             user_id=self.request.user.pk)
#         form.instance.writer = models.WriterUser.objects.get(
#             writer_user_id=pu.pk)
#
#         form.instance.event = models.Event.objects.get(pk=self.request.session['event_id'])
#         resp = super().form_valid(form)
#         c = models.Event.objects.get(pk=self.request.session['event_id'])
#         if c.singles_approved != c.singles_num:
#             c.singles_approved += 1
#             c.full_clean()
#             c.save()
#         elif c.singles_approved == c.singles_num:
#             resp = super().form_invalid(form)
#             form.add_error(None, "No more reply option left.")
#             # TODO check if no singles left before to try adding one..
#
#         # messages.SUCCESS(self.request, "event added successfully.") #TODO formating
#         return resp
#
#     def dispatch(self, request, *args, **kwargs):
#         self.request.session['event_id'] = kwargs['pk']
#
#         # if models.EventUser.objects.filter(event_user_id=request.user.pk).exists():
#         if self.request.session['is_matchmaker']:
#             return redirect("/")
#             # return reverse("events:event_details",
#             #         args=(self.request.session['event_id'],))
#
#         event_name = (models.Event.objects.get(pk=self.request.session['event_id'])).title
#         self.page_title += '"{}"'.format(event_name)
#
#         return super().dispatch(request, *args, **kwargs)
#
#
# class ReplyDetailView(LoggedInMixin, DetailView):
#     page_title = "Reply Details"
#     model = models.Reply
#
#
# class ListsinglesView(LoggedInMixin, ListView):
#     page_title = "singles list"
#     model = models.Reply
#     paginate_by = 5
#
#     def get_queryset(self):
#         # if self.request.user.is_authenticated():
#         if self.request.session['is_matchmaker']:
#             return super().get_queryset().filter(
#                 event=models.Event.objects.get(pk=self.request.session['event_id']))
#         elif self.request.session['is_single']:
#             return super().get_queryset().filter(
#                 writer=models.WriterUser.objects.get(
#                     writer_user_id=models.Profile.objects.get(
#                         user=self.request.user.pk)))

# class CreateProfileView(LoggedInMixin, CreateView):
#     page_title = "Edit Profile Details"
#     model = models.Profile
#     fields = (
#         'email'
#         'phone'
#     )
#
#     def get_initial(self):
#         f = super().get_initial()
#         f['']

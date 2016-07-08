from datetime import date

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Gender:
    MALE = 1
    FEMALE = 2

    choices = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )


class Status:
    SINGLE = 1
    DIVORCEE = 2
    DIVORCEE_WITH_KIDS = 3

    choices = (
        (SINGLE, 'single'),
        (DIVORCEE, 'divorcee'),
        (DIVORCEE_WITH_KIDS, 'divorcee with kids'),
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        unique=True,
        on_delete=models.CASCADE, )

    gender = models.IntegerField(choices=Gender.choices)
    status = models.IntegerField(choices=Status.choices, default=Status.SINGLE)
    dob = models.DateField(null=True, blank=True)
    is_cohen = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=MEDIA_ROOT, default=MEDIA_ROOT + '/no-image.jpg')

    # country = models.CharField(max_length=50, null=True, blank=True)
    # address = models.CharField(max_length=100, null=True, blank=True)
    # city = models.CharField(max_length=50, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)

    is_matchmaker = models.BooleanField(default=False)
    is_single = models.BooleanField(default=False)

    def calculate_age(self):
        age = 0
        today = date.today()
        if self.dob:
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    def __str__(self):
        return "{}".format(
            self.user.username,
        )


class Event(models.Model):
    owner = models.ForeignKey(Profile)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    link = models.URLField()
    date = models.DateField()
    singles_num = models.IntegerField(default=1)
    singles_approved = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("events:event_details", args=(self.pk,))

    def __str__(self):
        return "{}".format(
            self.title,
        )

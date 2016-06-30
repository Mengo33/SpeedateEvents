import re
from random import randint

import silly
from celery.utils.text import truncate
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from events import models
from events.models import Gender, Status


class Command(BaseCommand):
    help = "Generate silly users"

    def handle(self, *args, **options):
        n = 1000
        for i in range(n):
            user_name = "{}{}".format(re.sub('[^A-Za-z0-9]+', '', silly.name()), silly.number())
            email = silly.email()
            password = "{}{}".format(re.sub('[^A-Za-z0-9]+', '', silly.name()), silly.number())
            gender = Gender.MALE if round(i % 3, 1) == randint(0, 1) else Gender.FEMALE
            status = Status.DIVORCEE if round(i % 5, 1) == randint(0, 1) else Status.SINGLE
            dob = silly.datetime().date()
            is_cohen = True if round(i % 6, 1) == randint(0, 1) else False
            is_single = True
            # is_single = True if round(i % 3, 1) == randint(0, 1) else False
            try:
                user = User.objects.create_user("{}".format(user_name), email, password)
                # Add new user to ProfileUser
                pu = models.ProfileUser(
                    profile_user=user, gender=gender, status=status, dob=dob, is_cohen=is_cohen, is_single=is_single)
                pu.full_clean()
                pu.save()
            except():
                continue
        print("OK")

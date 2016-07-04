import re
from random import randint

import silly
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from events import models
from events.models import Gender, Status


class Command(BaseCommand):
    help = "Generate silly users"

    def handle(self, *args, **options):
        for i in range(100):
            user_name = re.sub('[^A-Za-z0-9]+', '', silly.name())
            email = silly.email()
            password = "{}{}".format(re.sub('[^A-Za-z0-9]+', '', silly.name()), silly.number())
            gender = Gender.MALE if i == randint(0, 100) else Gender.FEMALE
            status = Status.SINGLE if i == randint(0, 100) else Status.DIVORCEE
            dob = models.DateField()
            is_cohen = True if i == randint(0, 100) else False
            is_single = True if i == randint(0, 100) else False
            user = User.objects.create_user("{}".format(user_name), email, password)
            user.authenticate()
            # user = authenticate(**form.cleaned_data)
            # user.full_clean()
            # user.save()

            # Add new user to Profile
            pu = models.Profile(
                user=user, gender=gender, status=status, dob=dob, is_cohen=is_cohen, is_single=is_single)

            # pu.is_single = True
            pu.full_clean()
            pu.save()

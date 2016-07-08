import re
from random import randint

import silly
import tqdm as tqdm
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from events import models
from events.models import Gender, Status


class Command(BaseCommand):
    help = "Generate silly users"

    def get_silly_username(self):
        return "{}{}".format(re.sub('[^A-Za-z0-9]+', '', silly.name()), silly.number())

    def handle(self, *args, **options):
        n = 100
        for i in tqdm.tqdm(range(n)):
            try:
                user_name = self.get_silly_username()
                email = silly.email()
                password = self.get_silly_username()
                gender = Gender.MALE if randint(1, 3) == 3 else Gender.FEMALE
                status = Status.DIVORCEE if randint(1, 4) == 4 else Status.SINGLE
                dob = silly.datetime().date()
                is_cohen = True if randint(1, 6) == 6 else False
                picture = "text"
                while "placekitten" not in picture:
                    picture = silly.image(width=i+140*2, height=i+95*2).replace(" ", "%20")
                is_single = True

                # is_single = True if round(i % 3, 1) == randint(0, 1) else False
                user = User.objects.create_user("{}".format(user_name), email, password)
                # Add new user to Profile
                pu = models.Profile(
                    user=user,
                    gender=gender,
                    status=status,
                    dob=dob,
                    is_cohen=is_cohen,
                    is_single=is_single,
                    picture=picture,
                )
                pu.full_clean()
                pu.save()
            except IntegrityError:
                print("UNIQUE constraint failed: auth_user.username")
        print("OK")

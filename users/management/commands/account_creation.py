import argparse
import bz2
import csv
import os
import random
import time

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        with bz2.open(os.path.join(settings.BASE_DIR, "users", "words.bz2")) as f:
            self.words = [str(w.strip(), "utf-8") for w in f.readlines()]

    def add_arguments(self, parser):
        parser.add_argument("users_file", type=argparse.FileType('r'))

    def handle(self, *args, **options):

        for row in csv.reader(options["users_file"]):

            if not row:
                continue

            name = row[0]
            email = row[1]
            password = self._generate_password()

            User.objects.create(name=name, email=email)

            send_mail(
                "Your account on Export Wins has been created",
                "You can login with the following credentials:\n  Email: {}\n "
                " Password: {}".format(email, password),
                settings.SENDING_ADDRESS,
                (email,)
            )

            time.sleep(1)

    def _generate_password(self):
        separator = random.choice(("-", ",", ".", "_"))
        return "{}{}{}{}{}{}{}".format(
            random.choice(self.words),
            separator,
            random.choice(self.words),
            separator,
            random.choice(self.words),
            separator,
            random.choice(self.words),
        )

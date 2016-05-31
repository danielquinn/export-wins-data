import argparse
import bz2
import csv
import os
import random
import time

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from ...models import User


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.words = self._get_words()

        self.do_mail = True

    def add_arguments(self, parser):

        parser.add_argument("--name", type=str)
        parser.add_argument("--email", type=str)
        parser.add_argument(
            "--from-file",
            type=argparse.FileType('r'),
            help='The path to a CSV file in the following format: '
                 '"name","email".  This option is exclusive to use of --name '
                 'and --email.'
        )
        parser.add_argument(
            "--print",
            action="store_true",
            help="Don't generate and send email to the user.  Instead, just "
                 "print out their username & password to stdout."
        )

    def handle(self, *args, **options):

        if not (options["name"] and options["email"]):
            if not options["from_file"]:
                raise CommandError(
                    "Either --from-file or a combination of --name and "
                    "--email are required"
                )

        if options["print"]:
            self.do_mail = False

        if options["from_file"]:
            for row in csv.reader(options["from_file"]):
                if row:
                    self._handle_row(row)
            return

        password = self._generate_password()
        self._create_user(
            options["name"].strip(),
            self._sanitise_email(options["email"]),
            password
        )

    def _sanitise_email(self, address):
        address = address.strip().lower()
        validate_email(address)
        return address

    def _handle_row(self, row):

        name = row[0].strip()
        email = self._sanitise_email(row[1])
        password = self._generate_password()

        self.stdout.write("Sending mail to {}".format(name))
        self._create_user(name, email, password)

    @staticmethod
    def send(email, password):
        """
        This should probably be generated from a template, but this isn't a
        permanent use thing so I didn't bother.
        """

        send_mail(
            "Export Wins Login Credentials",
            "Dear Colleague\n\nThank you for agreeing to test the new "
            "Export Wins service.\n\nThis service is being developed with "
            "feedback from live user testing. It will be delivered in two "
            "parts: the first part is to be completed online by the Lead "
            "Officer in UKTI or FCO who has helped the Customer deliver "
            "the win. In the second part, the Customer will be sent an "
            "email, inviting them to confirm the Export Win.\n\nInitially "
            "we are only testing the functionality the first part of this "
            "process. Your team will have the opportunity to comment on "
            "the process that enables customers to confirm Export Wins "
            "before we begin testing that part.\n\nThe service can be "
            "accessed by copying and pasting the address below into your "
            "internet browser, or by clicking on this link:\n\n  "
            "https://www.exportwins.ukti.gov.uk/\n\n"
            "You should login using these credentials:\n\n  Email: {}\n  "
            "Password: {}\n\nIf you experience a problem accessing or "
            "completing the form using the link above, please contact us "
            "by email using the feedback button in the service or at:"
            "\n\n  Email: ada.lovelace@ukti.gsi.gov.uk\n  Subject: Export "
            "Wins Feedback\n\nBest Regards\n\n"
            "The UKTI Digital Team".format(
                email,
                password
            ),
            settings.SENDING_ADDRESS,
            (email,)
        )

        time.sleep(1)

    def _generate_password(self):
        separator = random.choice(("-", ",", ".", "_"))
        return "{}{}{}{}{}{}{}".format(
            random.choice(self.words), separator,
            random.choice(self.words), separator,
            random.choice(self.words), separator,
            random.choice(self.words),
        )

    @staticmethod
    def _get_words():
        path = os.path.join(settings.BASE_DIR, "users", "words.bz2")
        with bz2.open(path) as f:
            return [str(w.strip(), "utf-8") for w in f.readlines()]

    def _create_user(self, name, email, password):

        user = User.objects.create(name=name, email=email)
        user.set_password(password)
        user.save()

        if self.do_mail:
            self.send(email, password)
        else:
            self.stdout.write(
                "\nThe credentials for {} are: \n"
                "  Email:    {}\n"
                "  Password: {}\n\n".format(name, email, password)
            )

        return user

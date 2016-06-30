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
        self.ignore_existing = True
        self.resend = False

    def add_arguments(self, parser):

        parser.add_argument("--name", type=str)

        parser.add_argument("--email", type=str)

        parser.add_argument(
            "--resend",
            action="store_true",
            help="If a given email address exists, reset the password. "
                 "Otherwise raise an exception."
        )

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
            help="Create user and password, but just print it don't send."
        )

    def handle(self, *args, **options):
        """ Handle command line flags, and then do the business """

        if not (options["name"] and options["email"]):
            if not options["from_file"]:
                raise CommandError(
                    "Either --from-file or a combination of --name and "
                    "--email are required"
                )

        if options["print"]:
            self.do_mail = False

        if options["resend"]:
            self.resend = True

        if options["from_file"]:
            return self._handle_batch(options["from_file"])

        return self._handle_single(options["name"], options["email"])

    def _handle_batch(self, file_handle):
        for row in csv.reader(file_handle):
            if row:
                self._handle_user(
                    row[0].strip(),
                    self._sanitise_email(row[1]),
                    self._generate_password()
                )

    def _handle_single(self, name, email):
        self._handle_user(
            name.strip(),
            self._sanitise_email(email),
            self._generate_password()
        )

    @staticmethod
    def _sanitise_email(address):
        address = address.strip().lower()
        validate_email(address)
        return address

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
            "\n\n  Email: exportwins@ukti.gsi.gov.uk\n  Subject: Export "
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
        """ Make a password from selection of random words """

        separator = random.choice(("-", ",", ".", "_"))
        return "{}{}{}{}{}{}{}".format(
            random.choice(self.words), separator,
            random.choice(self.words), separator,
            random.choice(self.words), separator,
            random.choice(self.words),
        )

    @staticmethod
    def _get_words():
        """ Get words for use in password from a pre-filtered file """

        path = os.path.join(settings.BASE_DIR, "users", "words.bz2")
        with bz2.open(path) as f:
            return [str(w.strip(), "utf-8") for w in f.readlines()]

    def _handle_user(self, name, email, password):
        """ Get or create the user, set password and either send or print """

        user, user_exists = self._get_or_create_user(name, email)

        if user_exists:
            if self.resend:
                print("Resending", user)
            elif self.ignore_existing:
                print("Ignoring", user)
                return
            else:
                raise Exception("user already exists")

        user.set_password(password)
        user.save()

        if self.do_mail:
            self.stdout.write("Sending mail to {}".format(name))
            self.send(email, password)
        else:
            self.stdout.write(
                "\nThe credentials for {} are: \n"
                "  Email:    {}\n"
                "  Password: {}\n\n".format(name, email, password)
            )

    def _get_or_create_user(self, name, email):
        try:
            user = User.objects.get(email=email)
            return (user, True)
        except User.DoesNotExist:
            # always want to create a new user if none exists
            user = User.objects.create(name=name, email=email)
            return (user, False)

from dateutil.relativedelta import relativedelta
from time import sleep

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from ...models import Win, Notification


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "limit",
            type=int,
            help="The number of customers to whom we will send invitations."
        )
        parser.add_argument(
            "--domain",
            type=str,
            default="www.exportwins.ukti.gov.uk",
            help="The domain to send the customers to."
        )

    def handle(self, *args, **options):

        two_weeks_ago = timezone.now() - relativedelta(weeks=2)

        unnotified_wins = Win.objects.filter(
            confirmation__isnull=True
        ).exclude(
            notifications__created__gte=two_weeks_ago,
            notifications__type=Notification.TYPE_CUSTOMER
        ).order_by(
            "created"
        )[:options["limit"]]

        for win in unnotified_wins:

            self.stdout.write("Sending email to {} ({})".format(
                win.customer_name, win.customer_email_address), ending=" ")

            send_mail(
                "Congratulations from {} on your export business "
                "success".format(win.user.name),
                render_to_string("wins/email/customer-notification.email", {
                    "win": win,
                    "url": "https://{}/wins/review/{}".format(
                        options["domain"],
                        win.pk
                    )
                }),
                settings.SENDING_ADDRESS,
                (win.customer_email_address,)
            )

            Notification.objects.create(
                win=win,
                recipient=win.customer_email_address,
                type=Notification.TYPE_CUSTOMER
            )

            sleep(0.5)

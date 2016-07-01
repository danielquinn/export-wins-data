from dateutil.relativedelta import relativedelta
from time import sleep

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from ...models import Win, Notification
from ...notifications import generate_customer_email, generate_officer_email


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--ids", type=str)
        parser.add_argument("--send", action="store_true",)

    def handle(self, *args, **options):
        """ Quick hack to generate txt of customer emails and corresponding
        officer emails.
        """

        given_win_ids = [w.replace('-', '') for w in options['ids'].split(',')]

        wins = Win.objects.filter(id__in=given_win_ids)
        found_win_ids = set(str(win.id).replace('-', '') for win in wins)
        missing_win_ids = set(given_win_ids) - found_win_ids
        assert not missing_win_ids, "missing win ids: %s" % missing_win_ids

        for win in wins:

            # should not be hardcoded
            url = "https://www.exportwins.ukti.gov.uk/wins/review/" + str(win.pk)
            customer_email_dict = generate_customer_email(url, win)
            send_mail(
                customer_email_dict['subject'],
                customer_email_dict['body'],
                settings.FEEDBACK_ADDRESS,
                customer_email_dict['to'],
            )
            customer_notification = Notification(
                type=Notification.TYPE_CUSTOMER,
                win=win,
                recipient=customer_email_dict['to'][0],
            )
            customer_notification.save()

            officer_email_dict = generate_officer_email(win)
            send_mail(
                officer_email_dict['subject'],
                officer_email_dict['body'],
                settings.SENDING_ADDRESS,
                officer_email_dict['to'],
            )
            for officer_email in officer_email_dict['to']:
                officer_notification = Notification(
                    type=Notification.TYPE_OFFICER,
                    win=win,
                    recipient=officer_email,
                )
                officer_notification.save()

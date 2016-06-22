from dateutil.relativedelta import relativedelta
from time import sleep

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from ...models import Win, Notification
from ...serializers import NotificationSerializer


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--ids", type=str)

    def handle(self, *args, **options):
        """ Quick hack to generate txt of customer emails and corresponding
        officer emails.
        """

        given_win_ids = options['ids'].split(',')

        wins = Win.objects.filter(id__in=given_win_ids)
        found_win_ids = set(str(win.id).replace('-', '') for win in wins)
        missing_win_ids = set(given_win_ids) - found_win_ids
        assert not missing_win_ids, "missing win ids: %s" % missing_win_ids

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('CUSTOMER EMAILS:')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        for win in wins:

            url = "https://www.exportwins.ukti.gov.uk/wins/review/" + str(win.pk)
            customer_email_dict = NotificationSerializer.generate_customer_email(
                url, win)

            print()
            print(', '.join(customer_email_dict['to']))
            print()
            print(customer_email_dict['subject'])
            print()
            print(customer_email_dict['body'])
            print()
            print('---------------------------------------------------')

        print('\n\n\n\n')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('ADVISOR EMAILS:')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('\n\n')

        for win in wins:
            officer_email_dict = NotificationSerializer.generate_officer_email(win)

            print()
            print(', '.join(officer_email_dict['to']))
            print()
            print(officer_email_dict['subject'])
            print()
            print(officer_email_dict['body'])
            print()
            print('---------------------------------------------------')

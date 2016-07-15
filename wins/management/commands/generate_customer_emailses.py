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
        parser.add_argument("--change_ids", type=str)

    def thing(self, given_win_ids):
        wins = Win.objects.filter(id__in=given_win_ids)
        found_win_ids = set(str(win.id).replace('-', '') for win in wins)
        missing_win_ids = set(given_win_ids) - found_win_ids
        assert not missing_win_ids, "missing win ids: %s" % missing_win_ids
        return wins

    def handle(self, *args, **options):
        """ Quick hack to generate txt of customer emails and corresponding
        officer emails.
        """

        if options['ids']:
            given_win_ids = [w.replace('-', '')
                             for w in options['ids'].split(',')]
            wins = self.thing(given_win_ids)
            change = False
        elif options['change_ids']:
            change = True
            idemails = options['change_ids']
            id_emails = [idemail.split(':')
                         for idemail in idemails.split(',') if idemail]
            id_to_email = {
                wid.replace('-', ''): email.lower()
                for wid, email in id_emails
            }
            wins = self.thing(list(id_to_email.keys()))

            for win in wins:
                win_id = str(win.id)
                new_customer_email = id_to_email[win_id.replace('-', '')]
                if win.customer_email_address != new_customer_email:
                    print(
                        'win', win_id,
                        'changing email from ',
                        win.customer_email_address,
                        'to',
                        new_customer_email,
                        'new email sent'
                    )
                    win.customer_email_address = new_customer_email
                    win.save()
                else:
                    print('win', win_id, 'customer email unchanged, email re-sent')

        else:
            assert False, 'no valid flag given'

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

            if not change:
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

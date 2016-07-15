from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Win


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--id", type=str)

    def handle(self, *args, **options):

        win_id = options['id'].replace('-', '')
        try:
            win = Win.objects.get(id=win_id)
        except Win.DoesNotExist:
            print('no such win')
        else:
            print(
                'win.id', win.id,
                'win.customer_email_address', win.customer_email_address,
                'win.customer_name', win.customer_name
            )

import json

from dateutil.relativedelta import relativedelta

from django.contrib.humanize.templatetags.humanize import intword
from django.core.management.base import BaseCommand
from django.db.models.aggregates import Sum
from django.utils import timezone

from users.models import User

from ...models import Win, CustomerResponse


class Command(BaseCommand):

    EXCLUDED_IDS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output the statistics in JSON format."
        )
        parser.add_argument(
            "--show-all",
            action="store_true",
            help="Don't exclude staff users."
        )

    def handle(self, *args, **options):

        wins = Win.objects.all()
        confirmations = CustomerResponse.objects.all()
        if not options["show_all"]:
            wins = wins.exclude(user__pk__in=self.EXCLUDED_IDS)
            confirmations = confirmations.exclude(
                win__user__pk__in=self.EXCLUDED_IDS)

        users = User.objects.all()
        one_week_ago = timezone.now() - relativedelta(weeks=1)

        stats = {
            "wins": {
                "total": wins.count(),
                "total-export-funds": wins.aggregate(
                    total=Sum("total_expected_export_value"))["total"],
                "total-non-export-funds": wins.aggregate(
                    total=Sum("total_expected_non_export_value"))["total"],
                "confirmed": confirmations.count()
            },
            "users": {
                "total-active": users.filter(
                    last_login__gt=one_week_ago).count(),
                "total-creating-wins": users.exclude(
                    wins__isnull=True).distinct().count()
            }
        }

        if options["json"]:
            return self._handle_json(stats)
        return self._handle_stdout(stats)

    def _handle_stdout(self, stats):

        wins = stats["wins"]
        users = stats["users"]

        self.stdout.write(
            "\n"
            "  Wins\n"
            "  -----------------------------------------\n"
            "    Total wins generated:   {:>15}\n"
            "    Total wins confirmed:   {:>15}\n"
            "    Total export funds:     {:>15}\n"
            "    Total non-export funds: {:>15}\n"
            "\n"
            "  Users\n"
            "  -----------------------------------------\n"
            "    Total currently active: {:>15}\n"
            "    Total ever active:      {:>15}\n"
            "\n".format(
                wins["total"],
                wins["confirmed"],
                "£{}".format(intword(wins["total-export-funds"])),
                "£{}".format(intword(wins["total-non-export-funds"])),
                users["total-active"],
                users["total-creating-wins"]
            ))

    @staticmethod
    def _handle_json(stats):
        return json.dumps(stats, separators={",", ":"})

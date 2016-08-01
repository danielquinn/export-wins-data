import collections
import csv
import functools
import io
import zipfile
from operator import attrgetter

from django.db import connection
from django.http import HttpResponse

from rest_framework import permissions
from rest_framework.views import APIView

from ..constants import BREAKDOWN_TYPES
from ..models import CustomerResponse, Win
from ..serializers import CustomerResponseSerializer, WinSerializer
from users .models import User


class CSVView(APIView):
    """ Endpoint returning CSV of all Win data, with foreign keys flattened """

    permission_classes = (permissions.IsAdminUser,)
    # cache for speed
    win_fields = WinSerializer().fields
    customerresponse_fields = CustomerResponseSerializer().fields

    def _extract_breakdowns(self, win):
        """ Return list of 10 tuples, 5 for export, 5 for non-export """

        breakdowns = win.breakdowns.all()
        retval = []
        for db_val, name in BREAKDOWN_TYPES:

            # get breakdowns of given type sorted by year
            type_breakdowns = [b for b in breakdowns if b.type == db_val]
            type_breakdowns = sorted(type_breakdowns, key=attrgetter('year'))

            # we currently solicit 5 years worth of breakdowns, but historic
            # data may have no input for some years
            for index in range(5):
                try:
                    breakdown = "{0}: {1}k".format(
                        type_breakdowns[index].year,
                        int(type_breakdowns[index].value / 1000),
                    )
                except IndexError:
                    breakdown = None

                retval.append((
                    "{0} breakdown {1}".format(name, index + 1),
                    breakdown,
                ))

        return retval

    def _confirmation(self, win):
        """ Add fields for confirmation """

        if hasattr(win, 'confirmation'):
            confirmation = win.confirmation
        else:
            confirmation = None

        values = [('customer response recieved', bool(confirmation))]
        for field_name in self.customerresponse_fields:
            if field_name in ['win', 'created']:
                continue
            model_field = self._get_customerresponse_field(field_name)
            if confirmation:
                if model_field.choices:
                    display_fn = getattr(
                        confirmation, "get_{0}_display".format(field_name)
                    )
                    value = display_fn()
                else:
                    value = getattr(confirmation, field_name)
            else:
                value = ''
            model_field_name = model_field.verbose_name or model_field.name
            values.append((model_field_name, str(value)))
        return values

    def _get_model_field(self, model, name):
        return next(
            filter(lambda field: field.name == name, model._meta.fields)
        )

    @functools.lru_cache(None)
    def _get_customerresponse_field(self, name):
        """ Get field specified in CustomerResponse model """
        return self._get_model_field(CustomerResponse, name)

    @functools.lru_cache(None)
    def _get_win_field(self, name):
        """ Get field specified in Win model """
        return self._get_model_field(Win, name)

    def _get_win_dict(self, win):
        """ Take Win instance, return ordered dict of {name -> value} """

        # want consistent ordering so CSVs are always same format
        win_dict = collections.OrderedDict()

        # local fields
        for field_name in self.win_fields:
            model_field = self._get_win_field(field_name)
            if model_field.choices:
                display_fn = getattr(
                    win, "get_{0}_display".format(field_name)
                )
                value = display_fn()
            else:
                value = getattr(win, field_name)

            model_field_name = model_field.verbose_name or model_field.name
            win_dict[model_field_name] = str(value)

        # remote fields
        win_dict['user'] = str(win.user)
        win_dict['contributing advisors/team'] = (
            ', '.join(map(str, win.advisors.all()))
        )
        win_dict['notifications'] = bool(win.notifications.filter(type='c'))
        win_dict.update(self._extract_breakdowns(win))
        win_dict.update(self._confirmation(win))

        return win_dict

    def _make_flat_wins_csv(self):
        """ Make CSV of all Wins, with non-local data flattened """

        wins = Win.objects.all(
        ).select_related(
            'user__id',
            'user__email',
        ).prefetch_related(
            'advisors',
            'breakdowns',
            'confirmation',
            'notifications',
        ).exclude(
            user__email__in=[
                'adam.malinowski@digital.bis.gov.uk',
                'daniel.quinn@digital.bis.gov.uk',
            ]
        )
        win_dicts = [self._get_win_dict(win) for win in wins]
        stringio = io.StringIO()
        csv_writer = csv.DictWriter(stringio, win_dicts[0].keys())
        csv_writer.writeheader()
        for win_dict in win_dicts:
            csv_writer.writerow(win_dict)
        return stringio.getvalue()

    def _make_user_csv(self):
        users = User.objects.all()
        user_dicts = [
            {'name': u.name, 'email': u.email, 'joined': u.date_joined}
            for u in users
        ]
        stringio = io.StringIO()
        csv_writer = csv.DictWriter(stringio, user_dicts[0].keys())
        csv_writer.writeheader()
        for user_dict in user_dicts:
            csv_writer.writerow(user_dict)
        return stringio.getvalue()

    def _make_plain_csv(self, table):
        """ Get CSV of table """

        stringio = io.StringIO()
        cursor = connection.cursor()
        cursor.execute("select * from wins_{};".format(table))
        csv_writer = csv.writer(stringio)
        header = [i[0] for i in cursor.description]
        csv_writer.writerow(header)
        csv_writer.writerows(cursor)
        return stringio.getvalue()

    def get(self, request, format=None):
        bytesio = io.BytesIO()
        zf = zipfile.ZipFile(bytesio, 'w')
        # for table in ['win', 'customerresponse', 'notification', 'advisor']:
        #     csv_str = self._make_plain_csv(table)
        #     zf.writestr(table + 's.csv', csv_str)
        full_csv_str = self._make_flat_wins_csv()
        zf.writestr('wins_complete.csv', full_csv_str)
        user_csv_str = self._make_user_csv()
        zf.writestr('users.csv', user_csv_str)
        zf.close()
        return HttpResponse(bytesio.getvalue())

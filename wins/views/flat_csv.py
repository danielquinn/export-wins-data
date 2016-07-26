import collections
import csv
import io
import zipfile
from operator import attrgetter

from django.http import HttpResponse

from rest_framework import permissions
from rest_framework.views import APIView

from ..models import Win, CustomerResponse
from ..serializers import WinSerializer
from ..constants import BREAKDOWN_TYPES


class CSVView(APIView):
    """ Endpoint returning CSV of all Win data, with foreign keys flattened """

    permission_classes = (permissions.IsAdminUser,)

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

    def _get_win_field(self, name):
        """ Get field specified in Win model """

        return next(
            filter(lambda field: field.name == name, Win._meta.fields)
        )

    def _get_win_dict(self, win):
        """ Take Win instance, return ordered dict of {name -> value} """

        # want consistent ordering so CSVs are always same format
        win_dict = collections.OrderedDict()

        # local fields
        for field_name in WinSerializer().fields:
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
        win_dict['advisors'] = ', '.join(map(str, win.advisors.all()))
        win_dict['notifications'] = bool(win.notifications.filter(type='c'))
        try:
            getattr(win, 'confirmation')
            confirmed = True  # just record if customer has responded for now
            # if response.agree_with_win is None:
            #     confirmed = 'N/A'
            # else:
            #     confirmed = response.agree_with_win
        except CustomerResponse.DoesNotExist:
            confirmed = False
        win_dict['confirmation'] = confirmed
        win_dict.update(self._extract_breakdowns(win))

        return win_dict

    def _make_csv(self):
        """ Make CSV of all Wins """

        wins = Win.objects.all()
        win_dicts = [self._get_win_dict(win) for win in wins]
        stringio = io.StringIO()
        csv_writer = csv.DictWriter(stringio, win_dicts[0].keys())
        csv_writer.writeheader()
        for win_dict in win_dicts:
            csv_writer.writerow(win_dict)
        return stringio.getvalue()

    def get(self, request, format=None):
        bytesio = io.BytesIO()
        zf = zipfile.ZipFile(bytesio, 'w')
        csv_str = self._make_csv()
        zf.writestr('wins.csv', csv_str)
        zf.close()
        return HttpResponse(bytesio.getvalue())

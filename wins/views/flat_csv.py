import collections
import csv
import io
import zipfile

from django.http import HttpResponse

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Win, Breakdown, Advisor, CustomerResponse, Notification
from ..serializers import (
    WinSerializer, LimitedWinSerializer, BreakdownSerializer,
    AdvisorSerializer, CustomerResponseSerializer, NotificationSerializer
)


def flatten_user(attr):
    return "{0} <{1}>".format(attr.name, attr.email)


def flatten_advisors(attr):
    return ', '.join(map(str, attr.all()))


def flatten_breakdowns(attr):
    return ', '.join(map(str, attr.all()))


def flatten_notifications(attr):
    return any([x.type == 'c' for x in attr.all()])


class CSVView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer(self):
        return WinSerializer

    def metadata_class(self):
        serializer_metadata = metadata_class.get_serializer_info(serializer)
        return Response(serializer_metadata)

    def make_csv(self):
        """ Get CSV of table """
        fkeys = [
            ('user', flatten_user),
            ('advisors', flatten_advisors),
            ('breakdowns', flatten_breakdowns),
            ('notifications', flatten_notifications),
        ]
        stringio = io.StringIO()
        wins = Win.objects.all()
        win_dicts = []
        for win in wins:
            win_dict = collections.OrderedDict()

            # local fields
            for field in WinSerializer().fields:
                win_dict[field] = getattr(win, field)

            # remote fields
            for name, func in fkeys:
                win_dict.update([(name, func(getattr(win, name)))])

            try:
                getattr(win, 'confirmation') # customer response case
                win_dict.update([('confirmation', True)])
            except (CustomerResponse.DoesNotExist,) as exc:
                win_dict.update([('confirmation', False)])

            win_dicts.append(win_dict)

        csv_writer = csv.DictWriter(stringio, win_dicts[0].keys())
        csv_writer.writeheader()
        for win_dict in win_dicts:
            csv_writer.writerow(win_dict)
        return stringio.getvalue()

    def get(self, request, format=None):
        bytesio = io.BytesIO()
        zf = zipfile.ZipFile(bytesio, 'w')
        csv_str = self.make_csv()
        zf.writestr('wins.csv', csv_str)
        zf.close()
        return HttpResponse(bytesio.getvalue())

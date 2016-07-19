import collections
import csv
import io
import zipfile

from django.http import HttpResponse

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Win, Breakdown, Advisor, CustomerResponse, Notification
from ..serializers import WinSerializer

def join(attr):
    'Dumb flattening join for fkey'
    return ', '.join(map(str, attr.all()))

FKEY_FN = (
    ('user', lambda user: str(user)),
    ('advisors', join),
    ('breakdowns', join),
    ('notifications', lambda attr: any([x.type == 'c' for x in attr.all()])),
)

class CSVView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer(self):
        return WinSerializer

    def metadata_class(self):
        serializer_metadata = metadata_class.get_serializer_info(serializer)
        return Response(serializer_metadata)

    def make_csv(self):
        'Get CSV of table'
        wins = Win.objects.all()
        win_dicts = []
        for win in wins:
            win_dict = collections.OrderedDict()

            # local fields
            for field_name in WinSerializer().fields:
                try:
                    display_fn = getattr(
                        win, "get_{0}_display".format(field_name)
                    )
                    attr = display_fn()
                except AttributeError:
                    attr = getattr(win, field_name)
                win_dict[field_name] = str(attr)

            # remote fields
            for name, func in FKEY_FN:
                win_dict.update([(name, func(getattr(win, name)))])

            try:
                getattr(win, 'confirmation') # customer response case
                win_dict.update([('confirmation', True)])
            except (CustomerResponse.DoesNotExist,) as exc:
                win_dict.update([('confirmation', False)])

            win_dicts.append(win_dict)

        stringio = io.StringIO()
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

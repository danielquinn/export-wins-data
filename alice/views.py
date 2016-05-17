from rest_framework.decorators import list_route
from rest_framework.response import Response

from .authenticators import AlicePermission


class AliceMixin(object):

    permission_classes = (AlicePermission,)

    @list_route(methods=("get",))
    def schema(self, request):
        return Response(
            self.metadata_class().get_serializer_info(self.get_serializer()))

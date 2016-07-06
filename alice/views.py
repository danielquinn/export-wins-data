from rest_framework.decorators import list_route
from rest_framework.response import Response

from .authenticators import AlicePermission


class AliceMixin(object):
    """
    Mixin for ViewSets used by Alice clients which authenticate via Alice and
    reflect on schema view.
    """

    permission_classes = (AlicePermission,)

    @list_route(methods=("get",))
    def schema(self, request):
        """ Return metadata about fields of View's serializer """

        serializer = self.get_serializer()
        metadata_class = self.metadata_class()
        serializer_metadata = metadata_class.get_serializer_info(serializer)
        return Response(serializer_metadata)

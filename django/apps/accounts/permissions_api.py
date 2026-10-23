from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import catalog, has_permission


class PermissionCatalogApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not has_permission(request.user, "roles.view"):
            return Response(status=403)
        return Response(catalog())

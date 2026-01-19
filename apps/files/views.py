from django.db.models import QuerySet
from django.http import FileResponse
from rest_framework import permissions, views, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import UserFile
from .serializers import UserFileSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: views.APIView, obj: UserFile) -> bool:
        return obj.owner == request.user


class UserFileViewSet(viewsets.ModelViewSet[UserFile]):
    serializer_class = UserFileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self) -> QuerySet[UserFile]:
        return UserFile.objects.filter(owner=self.request.user)  # type: ignore[misc]

    @action(detail=True, methods=["get"])
    def download(self, request: Request, pk: None = None) -> Response | FileResponse:
        user_file = self.get_object()
        response = FileResponse(user_file.file.open(), as_attachment=True, filename=user_file.name)
        return response

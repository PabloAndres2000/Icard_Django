from ctypes.wintypes import HLOCAL
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from icard.apps.users.api.serializers.user import UpdateSerializer, UserListSerializer, UserSignUpSerializer
from icard.apps.users.providers import user as user_providers
from icard.apps.users.utils.ip import get_client_ip
from icard.utils.constants import (
    DATA_NOT_FOUND,
    PERMISSIONS_ERROR,
    SERVER_ERROR,
    NOT_FILLED_FIELDS,
    WRONG_CREDENTIALS
)


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, url_name="me", url_path="me",)
    def me(self, request):
        user = request.user
        serializer = UserListSerializer(user)
        return Response(serializer.data)

    # POST: api/users/user/signup/
    @action(detail=False, methods=['post'], url_name="signup", url_path="signup")
    def signup(self, request):
        context = {"ip_address": get_client_ip(request)}
        serializer = UserSignUpSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"message": "Usuario creado con exito"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        if not pk:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if not user_providers.check_user_is_owner_or_staff(request_user=request.user, user_pk=pk):
            return Response(PERMISSIONS_ERROR, status=status.HTTP_403_FORBIDDEN)
        user = user_providers.get_user_by_pk(pk=pk)
        if not user:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Usuario actualizado con exito"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

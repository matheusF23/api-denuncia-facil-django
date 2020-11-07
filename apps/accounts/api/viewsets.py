from django.contrib.auth import authenticate, get_user_model

from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import permissions
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permissions.UpdateOwnUser)

    @action(methods=['post', ], detail=False, permission_classes=[], authentication_classes=[])
    def login(self, request, *args, **kwargs):
        is_missing, field = missing_fields(request.data, 'password', 'email')
        if is_missing:
            return Response({"message": f"Campo '{field}' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=request.data['email'],
                            password=request.data['password'])
        if user:
            serializer = self.get_serializer(user)
            return Response({**serializer.data})

        return Response({"message": "Senha ou email inválidos"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', ], detail=False, permission_classes=[], authentication_classes=[])
    def register(self, request, *args, **kwargs):
        is_missing, field = missing_fields(request.data, 'password', 'email')
        if is_missing:
            return Response({"message": f"{field} é obrigatório"},
                            status=status.HTTP_400_BAD_REQUEST)

        if get_user_model().objects.filter(email=request.data['email']).exists():
            return Response({"message": f"email '{request.data['email']}' já existe."},
                            status=status.HTTP_409_CONFLICT)
        res = self.create(request, *args, **kwargs)
        return res

    @action(methods=['put', 'patch', ], detail=False, permission_classes=[IsAuthenticated, permissions.UpdateOwnUser], authentication_classes=[TokenAuthentication])
    def updateprofile(self, request, *args, **kwargs):
        params = request.data
        email = params.get("email", None)
        password = params.get("password", None)

        if email:
            return Response({"message": "O email não pode ser alterado"},
                            status=status.HTTP_400_BAD_REQUEST)

        if password:
            return Response({"message": "A senha não pode ser alterada por esta requisição"},
                            status=status.HTTP_400_BAD_REQUEST)

        get_user_model().objects.filter(email=request.user.email).update(**params)
        user = get_user_model().objects.get(email=request.user.email)
        return Response(dict(
            name=user.name,
            cellphone=user.cellphone
        ), status=status.HTTP_200_OK)


def missing_fields(data: dict, *fields):
    for field in fields:
        if not data.get(field, None):
            return True, field
    return False, None

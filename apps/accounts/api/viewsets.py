from django.contrib.auth import authenticate, get_user_model

from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import permissions
from .serializers import UserDetailSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserDetailSerializer
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

    @action(methods=['put','patch', ], detail=False, permission_classes=[IsAuthenticated], authentication_classes=[TokenAuthentication])
    def update_profile(self, request, *args, **kwargs):
        params = request.data
        email = params.get("email", None)
        if email:
            return Response({"message": "Não pode alterar o email"},
                            status=status.HTTP_400_BAD_REQUEST)
        res = self.update(request, *args, **kwargs)
        return res



def missing_fields(data: dict, *fields):
    for field in fields:
        if not data.get(field, None):
            return True, field
    return False, None

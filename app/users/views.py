from rest_framework import generics, permissions
from rest_framework.response import Response

from app.users.models import User
from app.users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Регистрация прошла успешно!",
                    "data": serializer.data
                }
                return Response(data=response)
            else:
                data = serializer.errors
                return Response({"message": "Что-то пошло не так!",
                                 "data": data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

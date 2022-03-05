from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import RegisterUserSerializer

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckDuplicatedId(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id = request.data['id']
        try:
            user = User.objects.get(user_id=id)
            if (user):
                return Response(dict(result=True))
            else:
                return Response(dict(result=False))
        except:
            return Response(dict(result=False))


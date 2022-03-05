from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import RegisterUserSerializer
from papers.models import PaperUser


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserId(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.GET.get("username", None)
        user = User.objects.filter(username=username)
        if (user):
            return Response({"user_id" : user[0].id})
        else :
            return Response({"user_id": "None user found"})


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

class MyProfile(APIView):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        # 푼 시험지 전체 queryset
        paper_user_queryset = PaperUser.objects.filter(user=user).order_by('id')
        # 푼 시험지 id 목록
        paper_list = paper_user_queryset.values_list('id', flat=True)
        # 도장 개수
        stamp_counts = [0, 0, 0]
        for paper_user in paper_user_queryset:
            if (paper_user.total_score >= 80) :
                stamp_counts[0] += 1
            elif (paper_user.total_score >= 50) :
                stamp_counts[1] += 1
            else :
                stamp_counts[2] += 1

        result = {
            "username": user.username,
            "paper_count": paper_user_queryset.count(),
            "paper_list" : paper_list,
            "stamp_counts": stamp_counts
        }

        return Response(result)

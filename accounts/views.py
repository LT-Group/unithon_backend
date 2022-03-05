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
        # 회원가입 시 지정한 username으로 DB에 저장된 user id 를 return
        username = request.GET.get("username", None)
        user = User.objects.filter(username=username)
        if (user):
            return Response({"user_id" : user[0].id})
        else :
            return Response({"user_id": "None user found"})


class CheckDuplicatedId(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 아이디 중복확인
        id = request.data['id']
        try:
            user = User.objects.get(username=id)
            if (user):
                return Response(dict(result=True))
            else:
                return Response(dict(result=False))
        except:
            return Response(dict(result=False))


class MyProfile(APIView):

    def get(self, request, user_id):
        # 내 프로필에 들어가는 정보 (푼 시험지 수, 푼 시험지 목록, 전체 시험 평균, 받은 도장 수)
        user = User.objects.get(pk=user_id)
        # 푼 시험지 전체 queryset
        paper_user_queryset = PaperUser.objects.filter(user=user).order_by('id')
        total_score_list = list(paper_user_queryset.values_list('total_score', flat=True))
        if (total_score_list):
            total_score_avg = int((sum(total_score_list))/len(total_score_list))
        else :
            total_score_avg = None
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
            "total_score_avg": total_score_avg,
            "paper_count": paper_user_queryset.count(),
            "paper_list" : paper_list,
            "stamp_counts": stamp_counts
        }

        return Response(result)

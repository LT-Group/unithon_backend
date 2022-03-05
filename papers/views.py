import random

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from accounts.models import User
from papers.models import Paper, PaperUser, Question, QuestionUser


class GetPaper(APIView):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        #유저가 푼 시험 수
        user_paper_count = PaperUser.objects.filter(user=user).count()

        #유저가 푼 시험지 제외
        paper_queryset = Paper.objects.all()
        exclude_paper_list = []
        for paper in paper_queryset:
            if PaperUser.objects.filter(user=user, paper=paper):
                exclude_paper_list.append(paper.pk)

        paper_queryset = paper_queryset.exclude(pk__in=exclude_paper_list)

        #제외한 시험지 중 랜덤 시험지 추출
        paper_left = paper_queryset.count()
        if (paper_left):
            n = random.randint(0, paper_left-1)
            paper = paper_queryset[n]
            if paper.test_audio_file:
                file_url = paper.test_audio_file.url
            else :
                file_url = None
            #시험지 id 와
            return Response({
                "paper_id": paper.id,
                "user_paper_queryset" : user_paper_count + 1,
                "file": file_url
            })

        return Response({"result": "None_Paper_Left"})

class PostPaper(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.get(pk=data['user'])
        paper = Paper.objects.get(pk=data['paper'])
        question_list = paper.question.order_by('pk')

        paper_user = PaperUser.objects.create(user=user,paper=paper)

        # 채점
        is_correct = []
        answer_list = []
        score = 0
        for i in range(0,5):
            user_answer = data['answer'][i].split()
            answer = question_list[i].answer.split(' ')
            answer_list.append(question_list[i].answer)
            if (user_answer==answer):
                is_correct.append(True)
                score += 20
                QuestionUser.objects.create(user=user, question=question_list[i]
                                            ,answer_user=data['answer'][i]
                                            ,is_correct=True)
            else:
                is_correct.append(False)
                QuestionUser.objects.create(user=user, question=question_list[i]
                                            ,answer_user=data['answer'][i]
                                            ,is_correct=False)

        #고객이 푼 시험 점수 저장
        paper_user.total_score = score
        paper_user.save()

        result = {
            "score": score,
            "is_correct": is_correct,
            "answer": answer_list
        }
        return Response(result)

class GetPaperDetail(APIView):
    def get(self, request, user_id, paper_id):
        user = User.objects.get(pk=user_id)
        paper = Paper.objects.get(pk=paper_id)

        try:
            paper_user = PaperUser.objects.filter(user=user, paper=paper)[0]
        except:
            #유저가 해당 문제를 풀지 않은 경우
            return Response({"result": "None Paper Results"})

        question_queryset = paper.question.all().order_by('id')
        is_correct_list = []
        answer_user = []
        answer = []

        for question in question_queryset:
            question_user = question.question_user.filter(user=user)[0]
            # 정답 여부
            is_correct_list.append(question_user.is_correct)
            # 유저가 쓴 정답
            answer_user.append(question_user.answer_user)
            # 실제 정답
            answer.append(question.answer)

        return Response({
            "username": user.username,
            "created_at": paper_user.created_at.strftime("%Y-%m-%d"),
            "score": paper_user.total_score,
            "is_correct_list": is_correct_list,
            "answer_user": answer_user,
            "answer": answer
        })


class PageCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"page_count": PaperUser.objects.count()})

class QuestionRank(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        question_list = Question.objects.order_by('-wrong_answer_rate')[:10]

        ranking_list = []
        i = 0
        for question in question_list:
            i += 1
            ranking_list.append({
                "rank": i,
                "question": question.answer,
                "wrong_answer_rate" : round(question.wrong_answer_rate * 100 , 1)
            })

        return Response(ranking_list)


class SavingPaper(APIView):
    def post(self, request):
        for data in request.data:
            paper = Paper.objects.create()
            for answer in data:
                Question.objects.create(paper=paper, answer=answer)
        return Response(True)
from django.urls import path

from papers.views import *

app_name = 'papers'

urlpatterns = [
    path('get_paper/<int:user_id>/', GetPaper.as_view(), name="get_paper"),
    path('post_paper/', PostPaper.as_view(), name="post_paper"),
    path('get_paper_detail/<int:user_id>/<int:paper_id>/', GetPaperDetail.as_view(), name="get_paper_detail"),
    path('page_count/', PageCount.as_view(), name="page_count"),
    path('saving_paper/', SavingPaper.as_view(), name="saving_paper"),
    path('question_rank/', QuestionRank.as_view(), name="question_rank"),
    path('count_paperuser/<int:user_id>/', CountingPaperUser.as_view(), name="count_paperuser")
    
]



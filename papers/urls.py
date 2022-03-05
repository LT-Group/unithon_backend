from django.urls import path

from papers.views import GetPaper, SavingPaper, PostPaper, GetPaperDetail

app_name = 'papers'

urlpatterns = [
    path('get_paper/<int:user_id>/', GetPaper.as_view(), name="get_paper"),
    path('post_paper/', PostPaper.as_view(), name="post_paper"),
    path('get_paper_detail/<int:user_id>/<int:paper_id>/', GetPaperDetail.as_view()),
    path('saving_paper/', SavingPaper.as_view(), name="saving_paper"),
]
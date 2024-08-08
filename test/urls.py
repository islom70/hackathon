from django.urls import path
from .views import QuizListView, QuizDetailView, SubmitResponseView, EvaluateQuizView, QuizResultView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/evaluate/', EvaluateQuizView.as_view(), name='evaluate-quiz'),
    path('responses/submit/', SubmitResponseView.as_view(), name='submit-response'),
    path('quizzes/<int:quiz_id>/results/<int:user_id>/', QuizResultView.as_view(), name='quiz-results'),
]

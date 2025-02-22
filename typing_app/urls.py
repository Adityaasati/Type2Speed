from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('instructions/<str:exam_type>/', instruction_view, name="exam-instructions"),
    path('typing-test/<str:exam_type>/', typing_test_view, name="typing-test"),
    path('typing-test/<str:exam_type>/<int:passage_id>/', typing_test_view, name="typing-test-exam-specific"),
    path('typing-test/<str:exam_type>/<str:language>/<int:passage_id>/', typing_test_view, name="typing-test-cpct-specific"),
    path('feedback/', feedback_view, name="feedback"),
    path('test-result/<str:exam_type>/', test_result_view, name="test-result"),
    path("games/", typing_games_view, name="typing-games"),
    path("games/<str:game_name>/", typing_game_view, name="typing-game"),
    path("games/<str:game_name>/submit/", submit_typing_game_result, name="submit-typing-game"),
]











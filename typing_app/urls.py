from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('tips/', tips_view, name="tips"),
    path('tests/', tests_view, name="tests"),
    path("passages/<str:exam_type>/", passages_view, name="passages"),
    path("instructions/<str:exam_type>/<int:passage_id>/", instruction_view, name="instructions"),
    path("practise-instructions/<str:exam_type>/", practise_instruction_view, name="practise-instructions"),
    path('typing-test/<str:exam_type>/', typing_test_view, name="typing-test"),
    path('typing-test/<str:exam_type>/<int:passage_id>/', typing_test_view, name="typing-test-exam-specific"),
    path('typing-test/<str:exam_type>/<str:language>/<int:passage_id>/', typing_test_view, name="typing-test-exams"),
    path('feedback/', feedback_view, name="feedback"),
    path('test-result/<str:exam_type>/', test_result_view, name="test-result"),
    path("games/", typing_games_view, name="typing-games"),
    path("games/<str:game_name>/", typing_game_view, name="typing-game"),
    path("games/<str:game_name>/submit/", submit_typing_game_result, name="submit-typing-game"),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    
    
]











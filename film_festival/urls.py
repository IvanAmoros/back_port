from django.urls import path
from .views import FilmsToWatchList, FilmsWatchedList, RatingCreate, IncreaseUpVotes, MarkAsWatched


urlpatterns = [
    path('films-to-watch/', FilmsToWatchList.as_view()),
    path('films-watched/', FilmsWatchedList.as_view()),

    path('increase-up-votes/<int:film_id>/', IncreaseUpVotes.as_view()),
    path('mark-as-watched/<int:film_id>/', MarkAsWatched.as_view()),
    
    path('create-rating/<int:film_id>/', RatingCreate.as_view(), name='create-rating'),
]

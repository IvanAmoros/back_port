from django.urls import path
from .views import FilmsToWatchList, FilmsWatchedList, RatingCreate, IncreaseUpVotes, MarkAsWatched, UserRatedFilmsList, UserUpvotedFilmsList, GenreList


urlpatterns = [
    path('films-to-watch/', FilmsToWatchList.as_view()),
    
    path('films-watched/', FilmsWatchedList.as_view()),

    path('user-upvoted-films/', UserUpvotedFilmsList.as_view()),
    path('increase-up-votes/<int:film_id>/', IncreaseUpVotes.as_view()),

    path('genres/', GenreList.as_view()),

    path('mark-as-watched/<int:film_id>/', MarkAsWatched.as_view()),
    
    path('user-rated-films/', UserRatedFilmsList.as_view()),
    path('create-rating/<int:film_id>/', RatingCreate.as_view()),
]

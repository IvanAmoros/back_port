from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.utils import timezone
from django.db import IntegrityError

from .models import Film, Rating, Upvote, Provider, Genre
from .serializers import FilmToWatchSerializer, FilmWatchedSerializer, RatingSerializer, GenreSerializer


class FilmsToWatchList(ListAPIView):
    serializer_class = FilmToWatchSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super(FilmsToWatchList, self).get_permissions()

    def get_queryset(self):
        queryset = Film.objects.filter(watched=False).order_by('-total_upvotes', 'created')
        genres = self.request.query_params.getlist('genres')
        if genres:
            genre_objects = Genre.objects.filter(name__in=genres)
            queryset = queryset.filter(genres__in=genre_objects).distinct()
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            imdb_id = serializer.validated_data.get('imdb_id')
            if not imdb_id:
                return Response({'detail': 'The IMDb ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if Film.objects.filter(imdb_id=imdb_id).exists():
                return Response({'detail': 'This movie has already been proposed.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                film = serializer.save(proposed_by=request.user)
                providers_data = request.data.get('providers', [])
                for provider_data in providers_data:
                    provider, created = Provider.objects.get_or_create(
                        name=provider_data['name'],
                        defaults={'image_url': provider_data['image_url']}
                    )
                    film.providers.add(provider)
                genres_data = request.data.get('genres', [])
                for genre_name in genres_data:
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    film.genres.add(genre)
                return Response(FilmToWatchSerializer(film).data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'detail': 'This movie has already been proposed.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FilmsWatchedList(ListAPIView):
    queryset = Film.objects.filter(watched=True)
    serializer_class = FilmWatchedSerializer
    permission_classes = [AllowAny]


class GenreList(ListAPIView):
    queryset = Genre.objects.filter().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class RatingCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, film_id, format=None):
        film = get_object_or_404(Film, pk=film_id)
        user = request.user

        existing_rating = Rating.objects.filter(film=film, user=user).first()
        if existing_rating:
            return Response({'detail': 'You have already rated this film.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(film=film, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRatedFilmsList(ListAPIView):
    serializer_class = FilmWatchedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rated_films_ids = Rating.objects.filter(user=user).values_list('film_id', flat=True)
        return Film.objects.filter(id__in=rated_films_ids)


class UserUpvotedFilmsList(ListAPIView):
    serializer_class = FilmToWatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        upvoted_films_ids = Upvote.objects.filter(user=user).values_list('film_id', flat=True)
        return Film.objects.filter(id__in=upvoted_films_ids)


class IncreaseUpVotes(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, film_id):
        user = request.user
        film = get_object_or_404(Film, pk=film_id)

        if Upvote.objects.filter(user=user, film=film).exists():
            return Response({'detail': 'You have already upvoted this film.'}, status=status.HTTP_400_BAD_REQUEST)

        Upvote.objects.create(user=user, film=film)

        film.total_upvotes += 1
        film.save()

        return Response({'total_upvotes': film.total_upvotes}, status=status.HTTP_200_OK)


class MarkAsWatched(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, film_id):
        film = Film.objects.get(pk=film_id)
        if not film.watched:
            film.watched = True
            film.watched_date = timezone.now()
            film.save()
            return Response({'status': 'Film marked as watched', 'watched_date': film.watched_date}, status=status.HTTP_200_OK)
        return Response({'error': 'Film already marked as watched'}, status=status.HTTP_400_BAD_REQUEST)

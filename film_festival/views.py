from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.utils import timezone

from .models import Film, Rating
from .serializers import FilmToWatchSerializer, FilmWatchedSerializer, RatingSerializer

class FilmsToWatchList(ListAPIView):
    serializer_class = FilmToWatchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        This view should return a list of all the films that have not been watched yet.
        """
        return Film.objects.filter(watched=False).order_by('-up_votes')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilmsWatchedList(ListAPIView):
    queryset = Film.objects.filter(watched=True)
    serializer_class = FilmWatchedSerializer
    permission_classes = [AllowAny]
    

class RatingCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, film_id, format=None):
        film = get_object_or_404(Film, pk=film_id)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(film=film)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IncreaseUpVotes(APIView):
    permission_classes = [AllowAny]

    def post(self, request, film_id):
        film = Film.objects.get(pk=film_id)
        film.up_votes += 1
        film.save()
        return Response({'up_votes': film.up_votes}, status=status.HTTP_200_OK)
    

class MarkAsWatched(APIView):
    permission_classes = [AllowAny]

    def post(self, request, film_id):
        film = Film.objects.get(pk=film_id)
        if not film.watched:
            film.watched = True
            film.watched_date = timezone.now()
            print(timezone.now())
            print(film.watched_date)
            film.save()
            return Response({'status': 'Film marked as watched', 'watched_date': film.watched_date}, status=status.HTTP_200_OK)
        return Response({'error': 'Film already marked as watched'}, status=status.HTTP_400_BAD_REQUEST)
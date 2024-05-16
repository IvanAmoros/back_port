from rest_framework import serializers

from .models import Film, Rating

class FilmToWatchSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Film
        fields = ['id', 'tittle', 'image', 'description', 'total_upvotes', 'year', 'runtime', 'genre', 'director', 'actors', 'imdb_rating', 'imdb_votes', 'imdb_id']

    def __init__(self, *args, **kwargs):
        super(FilmToWatchSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields.pop('total_upvotes')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'stars']


class FilmWatchedSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    watched_date = serializers.DateField(format='%d/%m/%Y', default=None, allow_null=True)
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'tittle', 'image', 'description', 'watched_date', 'average_rating', 'vote_count', 'ratings', 'year', 'runtime', 'genre', 'director', 'actors', 'imdb_rating', 'imdb_votes']

    def get_vote_count(self, obj):
        return obj.ratings.count()
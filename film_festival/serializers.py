from rest_framework import serializers

from .models import Film, Rating, Provider, Genre


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'image_url']
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class UpvoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')
    class Meta:
        model = Rating
        fields = ['id', 'user']


class FilmToWatchSerializer(serializers.ModelSerializer):
    proposed_by = serializers.StringRelatedField(read_only=True)
    upvotes = UpvoteSerializer(many=True, read_only=True)
    providers = ProviderSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'tittle', 'image', 'description', 'total_upvotes', 'year', 'runtime', 'genre', 'director', 'actors', 'imdb_rating', 'imdb_votes', 'imdb_id', 'proposed_by', 'upvotes', 'providers', 'genres']

    def validate_imdb_id(self, value):
        if not value:
            raise serializers.ValidationError("The IMDb ID is required.")
        return value

    def __init__(self, *args, **kwargs):
        super(FilmToWatchSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields.pop('total_upvotes')


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')
    class Meta:
        model = Rating
        fields = ['id', 'stars', 'user']


class FilmWatchedSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    watched_date = serializers.DateField(format='%d/%m/%Y', default=None, allow_null=True)
    vote_count = serializers.SerializerMethodField()
    providers = ProviderSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'tittle', 'image', 'description', 'watched_date', 'average_rating', 'vote_count', 'ratings', 'year', 'runtime', 'genre', 'director', 'actors', 'imdb_rating', 'imdb_votes', 'providers', 'genres']

    def get_vote_count(self, obj):
        return obj.ratings.count()
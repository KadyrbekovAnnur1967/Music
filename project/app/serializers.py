from rest_framework import serializers
from app.models import Song, Genre
from app.tasks import parse_song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class SongParserSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if not attrs['author']:
            raise serializers.ValidationError(
                ('Укажите поле!')
            )
        return attrs
    
    def parsing(self):
        parse_song()
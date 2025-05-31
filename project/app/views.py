from app.serializers import GenreSerializer, SongSerializer, SongParserSerializer
from app.models import Genre, Song
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView, Response
from user.permissions import IsListener, IsRedactorOrAdmin
from user.models import CustomUser
from app.pagination import CustomPaginationSong




class SongListAPIView(ListAPIView):
    serializer_class = SongSerializer
    pagination_class = CustomPaginationSong

    def get_queryset(self):
        queryset = Song.objects.all()
        user = self.request.query_params.get('user')
        genre = self.request.query_params.get('genre')

        if user and genre:
            user_obj = CustomUser.objects.filter(email=user).first()
            genre_obj = Genre.objects.filter(genre=genre).first()
            queryset = Song.objects.filter(user=user_obj, genre=genre_obj)
        if user:
            user_obj = CustomUser.objects.filter(email=user).first()
            queryset = Song.objects.filter(user=user_obj)
        if genre:
            genre_obj = Genre.objects.filter(genre=genre).first()
            queryset = Song.objects.filter(genre=genre_obj)

        return queryset
        
class SongRetrieveAPIView(APIView):
    permission_classes = [IsListener, IsRedactorOrAdmin]

    def get(self, request, pk):
        queryset = Song.objects.get(pk=pk)
        serializer = SongSerializer(queryset, many=False)
        return Response(serializer.data, status=200)

class SongCreateAPIView(APIView):
    permission_classes = [IsRedactorOrAdmin]

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class SongUpdateAPIView(APIView):
    permission_classes = [IsRedactorOrAdmin]

    def put(self, request, pk):
        queryset = Song.objects.get(pk=pk)
        serializer = SongSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

class GenreListCreateAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class SongListCreateAPIView(ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongParserAPIView(APIView):

    def post(self, request):
        serializer_class = SongParserSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.parsing()
            return Response(f'Парсинг начался!')
        return Response('Произошла ошибка!')
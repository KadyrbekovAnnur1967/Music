from django.urls import path
from app.views import GenreListCreateAPIView, GenreRetrieveUpdateDestroyAPIView, \
    SongListCreateAPIView, SongRetrieveUpdateDestroyAPIView, SongParserAPIView, \
    SongListAPIView, SongCreateAPIView, SongRetrieveAPIView, SongUpdateAPIView \

urlpatterns = [
    path('genre_list_create/', GenreListCreateAPIView.as_view()),
    path('genre_retrieve_update_delete/<int:pk>/', GenreRetrieveUpdateDestroyAPIView.as_view()),
    path('song_list_create/', SongListCreateAPIView.as_view()),
    path('song_retrieve_update_delete/<int:pk>/', SongRetrieveUpdateDestroyAPIView.as_view()),
    path('parsing/', SongParserAPIView.as_view()),
    path('song_list/', SongListAPIView.as_view()),
    path('song_create/', SongCreateAPIView.as_view()),
    path('song_retrieve/<int:pk>/', SongRetrieveAPIView.as_view()),
    path('song_update/<int:pk>/', SongUpdateAPIView.as_view()),
]
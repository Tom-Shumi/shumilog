from django.urls import path
from . import views

app_name = 'movie'
urlpatterns = [
    path('review_list/', views.MovieReviewListView.as_view(), name='review_list'),
    path('review_search/', views.MovieReviewListView.as_view(), name='review_search'),
    path('review_detail/<int:id>', views.MovieReviewDetailView.as_view(), name='review_detail'),
    path('review_update/<int:id>', views.MovieReviewUpdateView.as_view(), name='review_update'),
    path('review_create/', views.MovieReviewCreateView.as_view(), name='review_create'),
    path('review_delete/', views.review_delete, name='review_delete'),
    path('search_movie_api/', views.search_movie_api, name='search_movie_api'),
    path('watch_later_list/', views.MovieWatchLaterListView.as_view(), name='watch_later_list'),
    path('watch_later_create/', views.MovieWatchLaterCreateView.as_view(), name='watch_later_create'),
    path('watch_later_delete/', views.watch_later_delete, name='watch_later_delete'),
    path('recommend_list/', views.MovieRecommendListView.as_view(), name='recommend_list'),
    path('recommend_search/', views.MovieRecommendListView.as_view(), name='recommend_search'),
    path('recommend_to_watch_later/', views.recommend_to_watch_later, name='recommend_to_watch_later'),
]

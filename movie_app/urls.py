from django.urls import path
from movie_app import views

urlpatterns = [
  # Director
  path('directors/', views.director_list_create_api_view),
  path('directors/<int:id>/', views.director_detail_api_view),
  
  # Movies
  path('movies/', views.movie_list_create_api_view),
  path('movies/<int:id>', views.movie_detail_api_view),
  
  # Reviews
  path('reviews/', views.review_list_create_api_view),
  path('reviews/<int:id>', views.review_detail_api_view),
  
  # Movies reviews
  path('movies/reviews/', views.movie_reviews_api_view)
]
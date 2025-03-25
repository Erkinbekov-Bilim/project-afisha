from django.urls import path
from movie_app import views

urlpatterns = [
  # Director
  path('directors/', views.DirectorListCreateApiView.as_view()),
  path('directors/<int:id>/', views.DirectorDetailApiView.as_view()),
  
  # Movies
  path('movies/', views.MovieListCreateApiView.as_view()),
  path('movies/<int:id>', views.MovieDetailApiView.as_view()),
  
  # Reviews
  path('reviews/', views.ReviewListCreateApiView.as_view()),
  path('reviews/<int:id>', views.ReviewDetailApiView.as_view()),
  
  # Movies reviews
  path('movies/reviews/', views.MovieReviewsApiView.as_view()),
]
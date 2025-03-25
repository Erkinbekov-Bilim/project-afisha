from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import (DirectorSerializer, 
                          DirectorDetailSerializer, 
                          MovieSerializer, 
                          MovieDetailSerializer,
                          ReviewSerializer, 
                          ReviewDetailSerializer, 
                          MovieValidationSerializer,
                          DirectorValidationSerializer, 
                          ReviewValidationSerializer)
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView


# Create your views here.


# Directors

class DirectorListCreateApiView(ListCreateAPIView):
  queryset = Director.objects.all()
  serializer_class = DirectorSerializer
  
  def post(self, request, *args, **kwargs):
    serializer = DirectorValidationSerializer(data = request.data)
    
    if not serializer.is_valid():
      return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    name = serializer.validated_data.get("name")
    
    director = Director.objects.create(name = name)
    data = DirectorSerializer(director).data
    
    return Response(data, status=status.HTTP_201_CREATED)
  
class DirectorDetailApiView(RetrieveUpdateDestroyAPIView):
  queryset = Director.objects.all()
  serializer_class = DirectorDetailSerializer
  lookup_field = 'id'
  
  def put(self, request, *args, **kwargs):
    serializer = DirectorValidationSerializer(data = request.data)
    
    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    director = self.get_object()
    
    director.name = serializer.validated_data.get("name")
    
    director.save()
    
    data = DirectorDetailSerializer(director).data
    
    return Response(data, status=status.HTTP_200_OK)
  
class MovieListCreateApiView(ListCreateAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  
  def post(self, request, *args, **kwargs):
    serializer = MovieValidationSerializer(data=request.data)
    
    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    title = serializer.validated_data.get('title')
    description = serializer.validated_data.get('description')
    duration = serializer.validated_data.get('duration')
    director_id = serializer.validated_data.get('director_id')
    
    with transaction.atomic():
      movie = Movie.objects.create(
        title = title,
        description = description,
        duration = duration,
        director_id = director_id
      )
      
    data = MovieSerializer(movie).data
    return Response(data, status = status.HTTP_201_CREATED)


class MovieDetailApiView(RetrieveUpdateDestroyAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieDetailSerializer
  lookup_field = 'id'
  
  def put(self, request, *args, **kwargs):
    serializer = MovieValidationSerializer(data = request.data)
    
    serializer.is_valid(raise_exception=True)
    
    movie = self.get_object()
    
    movie.title = serializer.validated_data.get('title')
    movie.description = serializer.validated_data.get('description')
    movie.duration = serializer.validated_data.get('duration')
    movie.director_id = serializer.validated_data.get('director_id')
    
    movie.save()
    
    data = MovieDetailSerializer(movie).data
    return Response(data, status=status.HTTP_201_CREATED)
  

class ReviewListCreateApiView(ListCreateAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer
  
  def post(self, request, *args, **kwargs):
    serializer = ReviewValidationSerializer(data = request.data)
    
    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    text = serializer.validated_data.get('text')
    stars = serializer.validated_data.get('stars')
    movie_id = serializer.validated_data.get('movie_id')
    
    with transaction.atomic():
      review = Review.objects.create(
        text = text,
        stars = stars,
        movie_id = movie_id
      )
      
    data = ReviewSerializer(review, many=False).data
    return Response(data, status=status.HTTP_201_CREATED)
  
  
class ReviewDetailApiView(RetrieveUpdateDestroyAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewDetailSerializer
  lookup_field = 'id'
  
  def put(self, request, *args, **kwargs):
    serializer = ReviewValidationSerializer(data = request.data)
    
    serializer.is_valid(raise_exception=True)
    
    review = self.get_object()
    
    review.text = serializer.validated_data.get('text')
    review.stars = serializer.validated_data.get('stars')
    review.movie_id = serializer.validated_data.get('movie_id')
        
    review.save()
    
    data = ReviewDetailSerializer(review).data
    return Response(data, status=status.HTTP_201_CREATED)
  
  
class MovieReviewsApiView(ListAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieDetailSerializer
  
  
# @api_view(['GET', 'POST'])
# def director_list_create_api_view(request):
  
#   if request.method == "GET":
#     directors = Director.objects.all()
#     data = DirectorSerializer(directors, many=True).data
#     return Response(data, status=status.HTTP_200_OK)

#   elif request.method == "POST":
#     serializer = DirectorValidationSerializer(data = request.data)
    
#     if not serializer.is_valid():
#       return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     name = serializer.validated_data.get("name")
    
#     director = Director.objects.create(name = name)
#     data = DirectorSerializer(director).data
    
#     return Response(data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def director_detail_api_view(request, id):
#   try:
#     director = Director.objects.get(id=id)
    
#   except Director.DoesNotExist:
#     return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == "GET":
#     data = DirectorDetailSerializer(instance = director).data
    
#     return Response(data, status=status.HTTP_200_OK)
  
#   elif request.method == "PUT":
#     serializer = DirectorValidationSerializer(data = request.data)
    
#     if not serializer.is_valid():
#       return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     director.name = serializer.validated_data.get("name")
    
#     director.save()
    
#     data = DirectorDetailSerializer(director).data
    
#     return Response(data, status=status.HTTP_201_CREATED)
  
#   elif request.method == "DELETE":
#     director.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# Movies
# @api_view(['GET', 'POST'])
# def movie_list_create_api_view(request):
  
#   if request.method == "GET":
#     movies = Movie.objects.all()
#     data = MovieSerializer(movies, many=True).data
#     return Response(data, status=status.HTTP_200_OK)
  
#   elif request.method == "POST":
    
    
#     serializer = MovieValidationSerializer(data=request.data)
    
#     if not serializer.is_valid():
#       return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     title = serializer.validated_data.get('title')
#     description = serializer.validated_data.get('description')
#     duration = serializer.validated_data.get('duration')
#     director_id = serializer.validated_data.get('director_id')
    
#     with transaction.atomic():
#       movie = Movie.objects.create(
#         title = title,
#         description = description,
#         duration = duration,
#         director_id = director_id
#       )
      
#     data = MovieSerializer(movie).data
#     return Response(data, status = status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail_api_view(request, id):
#   try:
#     movie = Movie.objects.get(id=id)
    
#   except Movie.DoesNotExist:
#     return Response(data={'error': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == "GET":
  
#     data = MovieDetailSerializer(instance = movie).data
#     return Response(data, status=status.HTTP_200_OK)
  
#   elif request.method == "PUT":
#     serializer = MovieValidationSerializer(data = request.data)
    
#     if not serializer.is_valid():
#       return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     movie.title = serializer.validated_data.get('title')
#     movie.description = serializer.validated_data.get('description')
#     movie.duration = serializer.validated_data.get('duration')
#     movie.director_id = serializer.validated_data.get('director_id')
    
#     movie.save()
    
#     data = MovieDetailSerializer(movie).data
#     return Response(data, status=status.HTTP_201_CREATED)
  
#   elif request.method == "DELETE":
#     movie.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# Reviews
# @api_view(['GET', 'POST'])
# def review_list_create_api_view(request):
  
#   if request.method == "GET":
#     reviews = Review.objects.all()
#     data = ReviewSerializer(reviews, many=True).data
#     return Response(data, status=status.HTTP_200_OK)
  
#   elif request.method == "POST":
    
#     serializer = ReviewValidationSerializer(data = request.data)
    
#     if not serializer.is_valid():
#       return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     text = serializer.validated_data.get('text')
#     stars = serializer.validated_data.get('stars')
#     movie_id = serializer.validated_data.get('movie_id')
    
#     with transaction.atomic():
#       review = Review.objects.create(
#         text = text,
#         stars = stars,
#         movie_id = movie_id
#       )
      
#     data = ReviewSerializer(review, many=False).data
#     return Response(data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#   try:
#     review = Review.objects.get(id=id)
    
#   except Review.DoesNotExist:
#     return Response(data={'error': "Review not found"}, status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == "GET":
  
#     data = ReviewDetailSerializer(instance = review).data
#     return Response(data, status=status.HTTP_200_OK)
  
#   elif request.method == "PUT":
    
#     serializer = ReviewValidationSerializer(data = request.data)
    
#     if not serializer.is_valid():
#       return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
#     review.text = serializer.validated_data.get('text')
#     review.stars = serializer.validated_data.get('stars')
#     review.movie_id = serializer.validated_data.get('movie_id')
        
#     review.save()
    
#     data = ReviewDetailSerializer(review).data
#     return Response(data, status=status.HTTP_201_CREATED)
  
#   elif request.method == "DELETE":
#     review.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def movie_reviews_api_view(request):
#   reviews = Movie.objects.all()
#   data = MovieDetailSerializer(reviews, many=True).data
#   return Response(data, status=status.HTTP_200_OK)
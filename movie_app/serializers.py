from rest_framework import serializers
from .models import Movie, Director, Review

# Director
class DirectorSerializer(serializers.ModelSerializer):
  
  movies_count = serializers.SerializerMethodField()
  
  class Meta:
    model = Director
    fields = 'id name movies_count'.split()
    
  def get_movies_count(self, director):
    return director.movies_count()

class DirectorDetailSerializer(serializers.ModelSerializer):
  
  movie_name = serializers.SerializerMethodField()
  class Meta:
    model = Director
    fields = '__all__'
    
  def get_movie_name(self, director):
    return director.get_name_movies()


# Review
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = 'id text stars'.split()
    
class ReviewDetailSerializer(serializers.ModelSerializer):
  
  movie = serializers.StringRelatedField()
  class Meta:
    model = Review
    fields = '__all__'
    
    
    
# Movie
class MovieDetailSerializer(serializers.ModelSerializer):
  
  director = serializers.StringRelatedField()
  reviews = ReviewSerializer(many=True)
  average_rating = serializers.SerializerMethodField( method_name='get_average_rating')
  class Meta:
    model = Movie
    fields = '__all__'
    
  def get_average_rating(self, movie):
    return movie.get_average_stars()
    
class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = 'id title description duration'.split()
    
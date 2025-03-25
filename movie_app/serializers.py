from rest_framework import serializers
from .models import Movie, Director, Review
from rest_framework.exceptions import ValidationError

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
    
class ReviewValidationSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100, min_length=5)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.IntegerField(min_value=1, required=False)
    
    def validate_movie_id(self, movie_id):
      print("movie_id", movie_id)
      try: 
        Movie.objects.get(id=movie_id)
        
      except Movie.DoesNotExist:
        raise ValidationError("Movie not found")
      return movie_id
    

class DirectorValidationSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100, min_length=5)
    
class MovieValidationSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=100, min_length=5)
  description = serializers.CharField(max_length=500, min_length=5)
  duration = serializers.IntegerField(min_value=1, max_value=500)
  director_id = serializers.IntegerField(min_value=1)
  reviews = serializers.ListField(child=ReviewValidationSerializer(), required=False)
  
  def validate_director_id(self, director_id):
    try: 
      Director.objects.get(id=director_id)
      
    except Director.DoesNotExist:
      raise ValidationError("Director not found")
    return director_id
  

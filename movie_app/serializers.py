from rest_framework import serializers
from .models import Movie, Director, Review

# Director
class DirectorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Director
    fields = 'id name'.split()
    

class DirectorDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Director
    fields = '__all__'




# Movie
class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = 'id title description duration'.split()
    
class MovieDetailSerializer(serializers.ModelSerializer):
  
  director = serializers.StringRelatedField()
  class Meta:
    model = Movie
    fields = '__all__'
    

# Review
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = 'text'.split()
    
class ReviewDetailSerializer(serializers.ModelSerializer):
  
  movie = serializers.StringRelatedField()
  class Meta:
    model = Review
    fields = '__all__'
from django.db import models
from django.db.models import Avg
# Create your models here.

class Director(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name
  
  def movies_count(self):
    return self.movies.count()
  
  def get_name_movies(self):
    return self.movies.values_list('title', flat=True)
  

class Movie(models.Model):
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=500)
  duration = models.IntegerField()
  director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies', null=True)
  
  
  def get_average_stars(self):
    average = self.reviews.aggregate(avg_stars = Avg('stars'))['avg_stars']
    return round(average, 1) if average else 0
  
  def __str__(self):
    return self.title
  
STARS = (
  (i, '*' * i) for i in range(1, 6)
)
  
class Review(models.Model):
  text = models.CharField(max_length=100)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
  stars = models.IntegerField(choices=STARS, default=5)
  
  def __str__(self):
    return self.text
  
from django.db import models
from django.contrib.auth.models import User
import string
import random

# Create your models here.
class ConfirmationCode(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  code = models.CharField(max_length=6, unique=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def generate_code(self):
    characters = string.digits + string.ascii_letters
    char = random.choices(characters, k=6)
    return ''.join(char)
  
  def save(self, *args, **kwargs):
    if not self.code:
      self.code = self.generate_code()
    return super().save(*args, **kwargs)
      
  def __str__(self):
    return self.code
  
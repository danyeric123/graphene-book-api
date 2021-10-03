from django.db import models
from django.db.models.fields import CharField, PositiveBigIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Book(models.Model):
  title= CharField(max_length=100)
  author = CharField(max_length=50)
  year_published=CharField(max_length=10)
  review = PositiveBigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
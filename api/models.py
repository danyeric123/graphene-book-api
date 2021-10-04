from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, PositiveBigIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields.related import ForeignKey 

# Create your models here.
class Author(models.Model):
  first_name = CharField(max_length=100)
  last_name = CharField(max_length=100)
  dob = DateField()

class Book(models.Model):
  title= CharField(max_length=100)
  author = ForeignKey('Author',on_delete=CASCADE)
  year_published=CharField(max_length=10)
  review = PositiveBigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
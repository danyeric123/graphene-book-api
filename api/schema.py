import graphene
from graphene.types.field import Field
from graphene.types.objecttype import ObjectType
from graphene.types.scalars import Int

from graphene_django import DjangoObjectType, DjangoListField
from .models import Book

class BookType(DjangoObjectType):
  class Meta:
    model = Book
    fields ='__all__'
    
class Query(ObjectType):
  all_books = graphene.List(BookType)
  book = Field(BookType, book_id=Int())
  
  def resolve_all_books(self, info, **kwargs):
    return Book.objects.all()
  
  def resolve_book(self,info, book_id):
    return Book.objects.get(pk=book_id)
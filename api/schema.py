import graphene
from graphene.types import field
from graphene.types.field import Field
from graphene.types.inputobjecttype import InputObjectType
from graphene.types.mutation import Mutation
from graphene.types.objecttype import ObjectType
from graphene.types.scalars import ID, Int, String
from graphene.types.schema import Schema

from graphene_django import DjangoObjectType, DjangoListField
from .models import Author, Book

class AuthorType(DjangoObjectType):
  class Meta:
    model = Author
    field = '__all__'

class BookType(DjangoObjectType):
  class Meta:
    model = Book
    fields = '__all__'
    
class Query(ObjectType):
  all_books = graphene.List(BookType)
  book = Field(BookType, book_id=Int())
  
  def resolve_all_books(self, info, **kwargs):
    return Book.objects.all()
  
  def resolve_book(self,info, book_id):
    return Book.objects.get(pk=book_id)
  
class BookInput(InputObjectType):
  id = ID()
  title = String()
  author = String()
  year_published= String()
  review = Int()
  
class CreateBook(Mutation):
  class Arguments:
    book_data = BookInput(required=True)
    
  book = Field(BookType)
  
  @staticmethod
  def mutate(root, info, book_data=None):
    book_instance =Book.objects.create(
      title=book_data.title,
      author= book_data.author,
      year_published=book_data.year_published,
      review = book_data.review
    )
    return CreateBook(book=book_instance)
  
class UpdateBook(Mutation):
  class Arguments:
    book_data = BookInput(required=True)
    
  book = Field(BookType)
  
  @staticmethod
  def mutate(root,info,book_data=None):
    
    book_instance = Book.objects.get(pk=book_data.id)
    
    if book_instance:
      if "title" in book_data: book_instance.title = book_data.title
      if "author" in book_data: book_instance.author = book_data.author
      if "year_published" in book_data: book_instance.year_published = book_data.year_published
      if "review" in book_data: book_instance.review = book_data.review
      book_instance.save()
      
      return UpdateBook(book=book_instance)
    return UpdateBook(book=None)
  
class DeleteBook(Mutation):
  class Arguments:
    id = ID()
    
  book = Field(BookType)
  
  @staticmethod
  def mutate(root,info, id):
    book_instance = Book.objects.get(pk=id)
    book_instance.delete()
    
    return None
    
class Mutation(ObjectType):
  create_book = CreateBook.Field()
  update_book = UpdateBook.Field()
  delete_book = DeleteBook.Field()
  
schema = Schema(query=Query, mutation=Mutation)
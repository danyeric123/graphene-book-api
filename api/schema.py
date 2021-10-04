from django.http import request
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
    
class AuthorInput(InputObjectType):
  id = ID()
  first_name = String()
  last_name = String()
  dob = graphene.Date()
  
class BookInput(InputObjectType):
  id = ID()
  title = String()
  author = Field(AuthorInput)
  year_published= String()
  review = Int()
    
class Query(ObjectType):
  all_books = graphene.List(BookType)
  book = Field(BookType, book_id=Int())
  book_by_author = Field(AuthorType,first_name=String(required=True),last_name=String(required=True))
  
  def resolve_all_books(self, info, **kwargs):
    return Book.objects.all()
  
  def resolve_book(self,info, book_id):
    return Book.objects.get(pk=book_id)
  
  def resolve_book_by_author(self,info,first_name,last_name):
    try:
      return Author.objects.get(first_name=first_name,last_name=last_name)
    except Author.DoesNotExist:
      return None
  
class CreateBook(Mutation):
  class Arguments:
    book_data = BookInput(required=True)
    
  book = Field(BookType)
  
  @staticmethod
  def mutate(root, info, book_data=None):
    print(book_data['author'])
    author,_ = Author.objects.get_or_create(**book_data['author'])
    print(author)
    book_instance =Book.objects.create(
      title=book_data.title,
      author= author,
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
      if "year_published" in book_data: book_instance.year_published = book_data.year_published
      if "review" in book_data: book_instance.review = book_data.review
      if "author" in book_data:
        author = book_data['author']
        author_instance, new = Author.objects.get_or_create(**author)
        print(new)
        print(author_instance)
        if new or book_instance.author != author_instance:
          print(author_instance)
          book_instance.author = author_instance
        else:
          if "first_name" in author: author_instance.first_name = author.first_name
          if "last_name" in author: author_instance.last_name = author.last_name
          if 'dob' in author: author_instance.dob = author.dob
          author_instance.save()
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
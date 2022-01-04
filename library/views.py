from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer
from .models import Book

# Create your views here.
class BooksView(APIView):
    """Class for Index and Post"""
    def get(self, request):
        """Index Books"""
        books = Book.objects.all()
        data = BookSerializer(books, many=True).data
        return Response(data)
    
    def post(self, request):
        """Create Books"""
        print(request.data)
        book = BookSerializer(data=request.data)
        if book.is_valid():
            book.save()
            return Response(book.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book.errors, status=status.HTTP_400_BAD_REQUEST)

# def index(request):
#     books = Book.objects.all()
#     data = { 'books': list(books.values()) }
#     return JsonResponse(data)

# def show(request, pk):
#     # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#get
#     book = Book.objects.get(pk=pk).as_dict()
#     return JsonResponse(book)

class BookDetailView(APIView):
    def get(self, request, pk):
        """Show one book"""
        book = get_object_or_404(Book, pk=pk)
        data = BookSerializer(book).data
        return Response(data)
    
    def delete(self, request, pk):
        """Deletes a book"""
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        """Update a Book"""
        # first we locate the book
        book = get_object_or_404(Book, pk=pk)
        # then we run our update through the serializer
        updated_book = BookSerializer(book, data=request.data)
        if updated_book.is_valid():
            updated_book.save()
            return Response(updated_book.data)
        return Response(updated_book.errors, status=status.HTTP_400_BAD_REQUEST)
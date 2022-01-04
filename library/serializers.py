# import serializers from the django rest framework
from rest_framework import serializers

# import our model
from .models import Book

# create our serializer class
# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
class BookSerializer(serializers.ModelSerializer):
    # define meta class
    class Meta:
        # specify the model from which to define the fields
        model = Book
        # define the fields to be returned
        fields = '__all__'
        # fields = ['title', 'author']
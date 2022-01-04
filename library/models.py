from django.db import models

# Create your models here.
class Book(models.Model):
    """Defines fields and methods of the Book resource model"""
    # define our fields here
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/instances/#str
    # here we'll set up our __str__ method and our as_dict method
    def __str__(self):
        """Returns a string depiction of the model"""
        return self.title
    
    # This will be used before we have a serializer in the 'show' method request
    def as_dict(self):
        """returns dictionary version of the Book instance"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }

# Django CRUD

## Objectives

By the end of this, developers should be able to:

- Use Django framework to:
  - Create a resource in a SQL database
  - Read one or many resources in a SQL database
  - Update a resource in a SQL database
  - Delete a resource in a SQL database
- Explain and use migrations and serializers

## Preparation

1. Create a psql database for the project with `createdb db-name`, or use the shell:
    1. Type `psql` (`psql -U postgres` on Windows) to get into interactive shell.
    2. Run `CREATE DATABASE <db-name>;`.
    3. Exit shell with `\q`.
2. Run `pipenv shell` in the virtual environment folder, `sei/django-env`.
3. Fork and clone this repository **into the virtual environment folder**.
 [FAQ](https://git.generalassemb.ly/ga-wdi-boston/meta/wiki/ForkAndClone)
1. Change into the repository directory.
2. Create and checkout to a new branch, `training`, for your work.

## SQL Database with Django

Let's look at how we can use the Django framework to build an API that can Create, Read,
Update, and Delete resources and respond to requests with JSON.

We will be using a SQL database called PostgreSQL for our database, one of the
most popular SQL databases out there!

## Code-Along: Setting Up Our App

1. Create Project

In terminal, we need to create our project. Run `django-admin startproject campus_crud .`.
This will create our main project folder.

> Note: Don't forget the `.` in your command so we don't have redundant nested
> folders.

2. Create App

We can have as many apps as we might want, but for now, we will just make one.
Let's make sure we're in our `django_crud` directory and create our first app.

Run `django-admin startapp first_app` to create our `first_app` app folder next
to the `campus_crud` folder.

Our directory should look like this:

```
- django-crud/
  - campus_crud/
    - settings.py
    - ... other files
  - first_app/
    - migrations/
    - apps.py
    - ... other files
  - README.md
  - Pipfile
  - manage.py
  - ... other files
```

3. Register our app

In  order for our `campus_crud` project to be able to use things in our `first_app`
app, we need to register `first_app` as an app on our project.

Open up `campus_crud/settings.py` and locate this code:

```py
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

There are a lot of defaults in here, like the admin side of our application we
will get to play with later.

To register `first_app`, we will just add it to this list.

```py
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our Apps
    'first_app'
]
```

4. Connect to DB

We'll need a new package to work with our database, so we'll need to install
that into our virtual environment.

Run `pipenv install psycopg2-binary`. We should see it added to `django-env/Pipfile`.

Once we have this package, we'll be able to tell Django to use PostgreSQL
instead of the default, which is a very minimalist database called SQLite3.

Open up `campus_crud/settings.py` and locate this code:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Currently, Django is defaulted to using this sqlite3 database. This would be
fine, but we want to use PostgreSQL instead.

Update the above to look like:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django-campus',
    }
}
```

The name of our database can be anything we want, but ideally it's something
that will make sense for our project.

> **Windows Note:** Windows users may need to provide a `USER` and `PASSWORD` as
> well as `ENGINE` and `NAME`. The `USER` will be `postgres`, and the `PASSWORD`
> will be the password you set up for your PostgreSQL user and use to sign into
> the PostgreSQL shell.

## Run the Server

We'll be learning quite a few new commands to work with Django. Once we have
our project, we are also provided a `manage.py` file. This is the file we'll
actually be running, and providing it different commands.

These commands will follow this structure: `python manage.py <command-name>`

The first one we'll run now is the `runserver` command. This will (you guessed
it!) run our server.

Run `python manage.py runserver` and you'll see that our server is running
on port 8000 by default. Navigate to `http://locahost:8000` in the browser
and you'll see Django's nice little welcome message. We did it! Time to build
the actual app.

> Note: You'll see a message like this when you run your server. Don't worry,
> we'll deal with this later.
>
> `You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.`

### Code-Along: Our First View

Navigate to the `first_app/views.py` file. This is where we will add our function
to handle a "view" of our app.

```py
# first_app/views.py
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse('<h1>Welcome to our campus! /ᐠ｡‸｡ᐟ\ﾉ</h1>')
```

Currently, our view is just returning an `HttpResponse` with some HTML in it to
the client who is requesting our index view. This is the simplest way to send
back information in response to a request. However, in order to use it we need
to make sure we import it from the `django.http` module into this file.

### Code-Along: Mapping URLs

Our view doesn't do anything without being connected to a URL, however. When we
connect these pieces, we talk about "mapping" our view to a URL endpoint. Our
URL will point to a certain view function that will be called when we reach the
URL.

Our URLs will be app-specific, not project-specific, which means this
functionality should go inside of our `first_app` folder. There's no file there yet
for handling our URLs, so let's make one. Create a file called `urls.py` inside
of `first_app`.

In here, we will import the `path` function from Django's modules to setup our
URL as well as our own custom views from our app. Then, we will create our
`urlpatterns` that will reference all of our available endpoints and what view
they map to.

```py
# first_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

For our index view, we are giving the `path` function `''` as the endpoint, so
this will be what we hit when we go to that "home" page of our app. In Express,
we may have used `'/'` for our "home" or "root" route, but in Django we just
put an empty string. If we tried to put `'/'`, we would get a "Page not found"
error when trying to reload the browser.

We are pointing this "home" path to `views.index` which is the function we want
run when we hit the endpoint. Finally, we give it a name just to identify it
for other parts of our Django application.

This is great, but our URL is only set up for our app, `first_app`. It's not
connected to our project yet, though! We have a `urls.py` file for our project
too. Open up `campus_crud/urls.py` and we will update it so it knows about the
URLs in our `first_app` app.

First, we need to import the `include` function from the `django.urls` module.
Then, we can add a path to the URLs of our project that points to the URLs in
our `first_app` app.

```py
# campus_crud/urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
  path('admin/', admin.site.urls),
  # Add the line below
  path('', include('first_app.urls'))
]
```

Once we add that to our project, we should be able to refresh our browser page
and see our message! Django will restart the server for us when
it sees a file change, so we don't need to close and restart the server
ourselves.

## Code-Along: Our First Model

Let's start building our campus's library! Just like we created our `first_app`
app, we're now going to create a `library` app to handle all the functionality
of our library. To do this we will make sure we're in our `django_crud`
directory and run `django-admin startapp library`.

> Note: Don't forget to register our `library` app in `campus_crud/settings.py` just like we did for our `first_app` app.

Now that we created our `library` app, it's time to make our first resource! We will be making a `Book` class for our book resource inside of `library/models.py`.

We want our `Book` to have the following fields:

- title (string)
- author (string)
- created_at (date)
- updated_at (date)

We will also give our `Book` a couple methods called `__str__` and `as_dict`
which will return String and Dictionary representations of our resources,
respectively.

Let's take a look at the documentation to see how to proceed:
- [Django Models](https://docs.djangoproject.com/en/3.0/topics/db/models/)
- [Django Model Field Reference](https://docs.djangoproject.com/en/3.0/ref/models/fields/)

### Migrations with Django

In order to use our model, we need to register it in our project's
`INSTALLED_APPS` list found in the `settings.py` file. Now, our app is actually
connected to the project and the database.

Whenever we make changes to the data in our database, we need to use something
called "migrations" to make sure those changes actually show up in our
database. That means for new models or changes to old ones, we will need to let
Django know there are changes to propagate over to the database.

Let's generate and run our migrations:
1. `python3 manage.py makemigrations`
2. `python3 manage.py migrate`

Here are the commands with which we should be familiar:
- `makemigrations`: responsible for generating the migrations based on changes
in your models
- `migrate`: actually runs those migrations to propagate changes
- `sqlmigrate`: will show us the SQL statements for the migrations
- `showmigrations`: will list migrations and their status

> "You should think of migrations as a version control system for your database schema. `makemigrations` is responsible for packaging up your model changes into individual migration files - analogous to commits - and `migrate` is responsible for applying those to your database."
>
> \- [Django Migration Commands](https://docs.djangoproject.com/en/3.0/topics/migrations/#the-commands)

## Django ORM

What is an ORM?
An ORM is an Object-relational Mapper and it is used to map our Django code to
our SQL database. We can take a look at the different ORM functions that Django
supplies us with in its [database API](https://docs.djangoproject.com/en/3.1/topics/db/queries/).

>**Model Managers**:
Any time we want to perform a query operation on a Model to retrieve model
objects from our database, it is done through a Manager object. Django adds a
Manager to every Model by default; that's the `objects` attribute we'll be using
later!

## Code-Along: The Django Shell

We've created our first Model, ran our Migrations, and talked about the Django
ORM. Now, lets try it out!

To open the Django shell we will run:

```py
python3 manage.py shell
```

Let's try making some books together.

## Code-Along: Index

We need to set up a few things to make an index request to our Books:

1. An index ["view"](https://docs.djangoproject.com/en/3.0/topics/http/views/) in `views.py`

2. A URL endpoint that displays our view
    1. Define URL endpoint on the `library` app
    2. Register `library` URLs to the `campus_crud` project

For our view, open up `library/views.py` and we will create a basic request that
returns all of our books to the front end.

>Views are really just **functions that take in web requests and return web
>responses**. Often, they are used for displaying information in the form of the
>front-end's user interface.

```py
def index(request):
    books = Book.objects.all()
    data = list(books.values())
    return JsonResponse(data)
```

Then, we can add our URL by creating a new file at `library/urls.py` and
registering our app's urls in `campus_crud/urls.py`.

>Our view doesn't do anything without being connected to a URL, however. When we
>connect these pieces, we talk about "mapping" our view to a URL endpoint.
>**Our URL will point to a certain view function that will be called when
>we reach the URL**.

```py
#library/urls.py
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='books'),
]


#campus_crud/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('first_app.urls')),
    path('books/', include('library.urls')),
]
```

Finally, test your endpoint by going to `http://localhost:8000/books` in the
browser.

## Code-Along: Show

Now that we have our index view going, it's time to make a view for showing
just one book.

We will add our new view inside of `library/views.py`.

## Pivot: The Django Rest Framework

When we are working with Django, we could go ahead and try to build an API with
CRUD abilities without any special tools. We've already accomplished this for
index and show.

However, we have tools at our disposal! Might as well use them. Let's install
our first special tool, the Django REST framework. DRF is going to provide us
with some time saving tools as well as a ton of functionality!

> Note: Forgot about REST? Here's a refresher:
> Representational state transfer (REST) is a software architectural style that
> defines a set of constraints to be used for creating Web services. Web
> services that conform to the REST architectural style, called RESTful Web
> services, provide interoperability between computer systems on the Internet.
> RESTful Web services allow the requesting systems to access and manipulate
> textual representations of Web resources by using a uniform and predefined
> set of stateless operations.
>
> https://en.wikipedia.org/wiki/Representational_state_transfer

One of the things we'll be able to do with the Django Rest Framework (DRF) is
group our views together into the patterns we used with Express. We'll have endpoints
like `/books` and `/books/:id` (written a little differently in Django land) that
will run different view logic depending on if we hit that endpoint with a certain
HTTP verb like GET or POST.

1. Run `pipenv install djangorestframework` to install this package into our
application.

If you open up `Pipfile`, you should see that we have a reference to this
package in that file under `[packages]`. When someone else clones our project
down, running `pipenv install` will run through this file and make sure all the
necessary dependencies are installed.

2. We need to add the rest framework to our project's installed apps. Open
`campus_crud/settings.py` and add `'rest_framework'` to the
`INSTALLED_APPS` list.

## Code-Along: Serializers

When working with the Django Rest Framework, we will want to use serializers to
help us display our data nicely.

What are serializers, you may ask:

> "In computer science, in the context of data storage, serialization is the
> process of translating data structures or object state into a format that can
> be stored or transmitted and reconstructed later."
>
> [Serialization - Wikipedia](https://en.wikipedia.org/wiki/Serialization)

For us, these will be special files that we can use in our views to translate
our Book resources into readable objects we can return to the client. The
django rest framework has a lot of information about how their serializers work:
- [Django Rest Framework Serializers API Documentation](https://www.django-rest-framework.org/api-guide/serializers/)
- [CDRF Docs - Serializer Class](http://www.cdrf.co/3.9/rest_framework.serializers/ModelSerializer.html)

Create a file in the `library` app folder called `serializers.py`.

Code along as we add some basic serialization for our book resource.

## Class Based Views

Let's change over our two views to use the Django Rest Framework. This will
involve changing our views to use classes.

We will use the documentation to help us:
- [Django Class Based Views Tutorial](https://www.django-rest-framework.org/tutorial/3-class-based-views/)
- [Django Rest Framework Views API Documentation](https://www.django-rest-framework.org/api-guide/views/)
- [CDRF Docs - APIView Class](http://www.cdrf.co/3.9/rest_framework.views/APIView.html)

### Code-Along: Index

Let's make some changes to our views imports first:

1. Remove the `django.http` import.
2. Add:
    1. `from rest_framework.views import APIView`
    2. `from rest_framework.response import Response`
    3. `from rest_framework import status`
    4. `from .serializers import BookSerializer`

We are importing three modules from the Django Rest Framework, as well as our
serializer file for our `Book` resource that we just made.

Before the rest framework, we had two separate functions we created, one for
`index` and another for `show`. What we will be able to do now is group our
requests together into classes so they are "REST"ful. So, we will have a group
of requests that go to `/books` (like index and create) and others that go to
`/books/:id` (like show, update, and delete). By telling Django what type of
request each one should be (GET, POST, etc.), we will be able to make our
views more powerful (and restful).

Step 1: Setting up the new views

For our index request, we can start off by making a class for the views that
will go to `/books`. Let's call this class `BooksView` and have it inherit from
`APIView`. Inside of it, we will define a view by using `get` as our function
name so it only works for GET requests.

Step 2: Serializing our Books

Our `get` function will look similar to our old `index` function, but with a
couple changes. First, we want to use our serialize to make sure our book data
is nice and formatted! Let's add a line where we send our books to the
serializer, making sure to let our serializer know that we are working with
many books.

Step 3: Return a RESTful response

Instead of returning a `JsonResponse` like we did previously, we can use the
`Response` to just send our data back using the Django Rest Framework. Let's
update our return to do this.

Step 4: Update our URLs

We have one final thing to do, and that's update our urls! Open up
`library/urls.py`, and change to importing the `BooksView` class. Then, we can
reference our first set of URLs like:

```py
path('', BooksView.as_view(), name='books')
```

> Note: This will register our index view, but turns out it will register any
> others if we had them as well! Later on we will add a `post` function to the
> `BooksView` class, and we won't need to update our URLs at all.

### Lab: Show

Now, try it on your own with `show`!

1. Create a new class called `BookDetailView`
2. Add a `get` function for the show request
3. Locate (`get_object_or_404`) and serialize your book
4. Return a `Response` to the client
5. Test!

> ##### A quick note on class-based views:
>
> The purpose of class-based views is to group our requests, to make them
>"restful" so we have a view class called `BooksView` that contains `get` and
>`post` functions, and will be used when make a request to `/books`. If we
>make a **GET** request, that `BooksView` class will point us to the `get` function,
>vise-versa with **POST**. Similarly, the BookDetailView class contains `get`,
>`patch`, and `delete` functions to handle **GET**, **PATCH**, and **DELETE**
>requests to `/books/:id`.

### Code-Along: Create

So far, we have only been working on requesting data from our database. We can
also make a POST request that will create books on the database for us.

The endpoint for our post request will go to `/books`, so we will nest it
inside of our current `BooksView` class.

Let's add this post view and have it do the following:

1. Create a book using our `BookSerializer`
2. Check if the book we created is valid based on our model
    1. If it is, we will save the book and return with a successful `Response`
    1. Otherwise, we will respond with an error

### Lab: Update and Delete

Time to finish up the last two RESTful views we need on our application.

1. Add `patch` and `delete` functions to your `BookDetailView` class view
2. For each, locate the desired book using the `pk`
3. For `patch`, research how to use our serializer for updating data
4. For `delete`, research how to delete a resource with Django
5. Return responses with either errors or successful HTTP statuses for each

## Bonus Lab: Concrete View Classes

In addition to the more broad `APIView` class, the Django rest framework also
offers more ["concrete" view classes](https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes) to better manage what our views do.

We could use these classes to structure our views into the two endpoints we
currently have:

- Views for endpoint `'/books'`
- Views for endpoint `'/books/:id'`

In order to accommodate the functionality we want at `'/books'`, which is for
index and create, we could use the `ListCreateAPIView` class.

For the `'/books/:id'` views, we want to be able to show, update, and delete.
For this functionality, we could use the `RetrieveUpdateDestroyAPIView` class.

Read up on these classes these more specific view classes and try implementing
them instead of using `APIView` in your application.

## Additional Resources

### Try More:

- [Class Based Views](https://www.django-rest-framework.org/tutorial/3-class-based-views/)

### Dive Deeper:

- [What is REST](https://restfulapi.net/)

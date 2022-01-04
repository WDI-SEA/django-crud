## Pipenv and Virtual Environments

We haven't talked about them yet, but virtual environments are essential when
working with Python applications. When you install packages with `pip`, you are
installing them globally. That means every project you create will use the same
packages and versions! This is generally not a good thing, since you may have
projects that use an older version of Django and will break if you suddenly
install the newest version.

We will **always** use virtual environments when working with Django, and only
left them out until now because we weren't working with any packages while
looking at Python on it's own.

Pipenv is a tool that can help you manage your virtual environments as you move
from project to project. That way, your projects will end up looking more like
this:

![pipenv diagram](https://media.git.generalassemb.ly/user/16103/files/ab165900-6db8-11ea-8f8d-e3f410d9c2b7)

### Code-Along: Setting Up a Virtual Environment

1. We should have `pipenv` installed from installfest. Confirm this by running `pipenv --version`. If you get an error, flag down an instructor.

2. Run `pipenv shell` to start our virtual environment. You should see an
indication of this to the left of the file system location:

`(django-crud) ~/sei/trainings/django-crud`

We are now in a virtual environment only for the files in the
`django-crud` folder. We can safely install packages like Django and know that
it will only exist in this project without affecting any others.

3. To get pipenv going on this project, run `pipenv install` inside of this directory.

> Note: Normally we could run this with a package name (and we will in a
> minute), but for now we can run it without anything to initialize pipenv.

After these two steps, we should have some new files: `Pipfile` and `Pipfile.lock`.

**`Pipfile`:** This holds references to the packages we have installed and what
version they should be. This is similar to the `package.json` we used in Node,
in that it will control what is installed when our project is set up. Right
now, our `Pipfile` is mostly empty, but after it's filled with packages it will
be used to guide package setup.

**`Pipfile.lock`:** This is generated when someone runs `pipenv install`, and
holds lots of detail on the specific versions of each pacakage that was
installed. This is important, especially if our `Pipfile` doesn't specify a
version for a package, and is similar to `package-lock.json` in Node.

4. Run `pipenv install django` to install the Django framework. You should see
it appear in the `Pipfile`:

```
[packages]
django = "*"
```

The `*` indicates that if we try to install from this `Pipfile`, any Django
version could be installed! That's not great.

5. Re-do! Run `pipenv install django==3.0` to have pipenv install a specific
version (3.0) of the Django framework.

Your `Pipfile` will override the old reference:

```
[packages]
django = "==3.0"
```
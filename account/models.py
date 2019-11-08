from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# class UserManager - provides the helper function for creating a user or
# creating a superuser
class UserManager(BaseUserManager):
    # password=None - in case you want to create an inactive user that dont
    # have password
    # extra_fields - take any of the extra functions that you've passed when
    # you call the create_user and pass them
    # as extra_fields. we can add additional fields, more flexible
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address.')
        # the way the management commands work is you can access the model that
        # the manager is for by just typing
        # self.model. is the same as creating a new user model and assigning it
        # to the user variable
        # you cant set the password here because it's encrypted
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using=self._db - its required for supporting multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        # we dont need extra_fields because we only will use this function in
        # command line with these arguments only
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign the user manager to the objects attribute
    objects = UserManager()

    # by default the username is not the email, this changes to be the email
    USERNAME_FIELD = 'email'

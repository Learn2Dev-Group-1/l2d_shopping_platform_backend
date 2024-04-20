from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
        NON_BINARY = 'N'
        PREFER_NOT_TO_SAY = 'P'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=Gender.choices, max_length=1)
    address = models.CharField(max_length=512)


class Seller(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )


class Buyer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
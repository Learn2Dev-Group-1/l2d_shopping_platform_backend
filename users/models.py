from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
        NON_BINARY = 'N'
        PREFER_NOT_TO_SAY = 'P'

    class UserType(models.TextChoices):
        BUYER = 'Buyer'
        SELLER = 'Seller'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=Gender.choices, max_length=1, null=True)
    address = models.CharField(max_length=512, null=True)
    user_type = models.CharField(choices=UserType.choices, max_length=6, default='Buyer')


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Overriding the default username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']  # Username will still be required if you want

    def __str__(self):
        return self.email

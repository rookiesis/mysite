from django.contrib.auth.models import AbstractUser
from django.db import models

# AbstractUser: 실존하지 않는 테이블


# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.username
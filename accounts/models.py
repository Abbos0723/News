from django.contrib.auth.models import User
from django.db import models


#class User(AbstractUser):
#   photo = models.ImageField()
#  data_of_birth = models.DateTimeField()
# address = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default='default.jpg')

    def __str__(self):
        return f'Profile for user {self.user.username}'

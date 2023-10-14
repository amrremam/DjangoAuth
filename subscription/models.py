from django.db import models

# Create your models here.


class Package(models.Model):
    name = models.CharField(max_length=70)
    price = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    packages = models.ManyToManyField(Package)

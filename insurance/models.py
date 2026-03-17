from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Insurance(models.Model):

    insurance_name = models.CharField(max_length=255, unique=True)
    policy_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="insurances", null=True, blank=True
    )
    policy_number = models.CharField(max_length=255, unique=True)
    policy_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.insurance_name} >> {self.policy_number} << PHP: {self.premium}"


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline
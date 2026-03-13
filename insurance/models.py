from django.db import models
from django.contrib.auth.models import User  # or your custom user model


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


class Modern(models.Model):
    name = models.CharField(max_length=255, unique=True)

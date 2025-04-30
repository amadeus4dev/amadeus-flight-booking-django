from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('MALE', '남성'), ('FEMALE', '여성')])
    email_address = models.EmailField(unique=True)

class PassportInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passports')
    number = models.CharField(max_length=20)  # 여권번호
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()  # 추가
    issuance_date = models.DateField()
    issuance_location = models.CharField(max_length=100)
    expiry_date = models.DateField()
    nationality = models.CharField(max_length=10)
    birth_place = models.CharField(max_length=100)
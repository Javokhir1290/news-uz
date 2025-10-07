# OTP -> One Time Password (6 talik kod)
import datetime

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_type', 2)  # oddiy foydalanuvchi

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone, password=None, **extra_fields):
        # bu yerda avtomatik qiymatlar beramiz
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)  # majburan admin

        user = self.create_user(phone, password, **extra_fields)
        return user





class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=56)
    phone = models.CharField(max_length=15, unique=True)
    user_type = models.SmallIntegerField(default=2, choices=[
        (1, 'Admin'), # Dashboardga kira oladigan odam
        (2, 'User'),  # Oddiy Saytdan ruyxatdan utadigan odam
    ], verbose_name="Admin(1), User(2)") # role

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['user_type']




class Otp(models.Model):
    mobile = models.CharField(max_length=15)
    key = models.CharField(max_length=256) # 6 talik kod -> shifrlash
    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    by = models.CharField(choices=[
        ('login', 'Login'),
        ('regis', 'Register'),
    ])
    extra = models.JSONField(default=dict)
    tries = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def check_date(self):
        now = datetime.datetime.now()
        if (now-self.created).total_seconds() > 180:
            return False
        return True

    def save(self, *args, **kwargs):
        if self.tries >= 3 :
            self.is_expired = True
        if self.is_confirmed:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)
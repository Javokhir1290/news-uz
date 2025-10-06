# OTP -> One Time Password (6 talik kod)
import datetime

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, phone, password, **extra_fields):
        user = self.model(
            phone=phone,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user


    def create_user(self, phone, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_superuser(self, phone=phone, password=password, **extra_fields)



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
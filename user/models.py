from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Status(models.TextChoices):
        new = 'new', 'Новый'
        active = 'active', 'Активный'
        disable = 'disable', 'Отключен'

    class Role(models.TextChoices):
        user = 'user', 'Обычный'
        admin = 'admin', 'Админ'
        manager = 'manager', 'Менеджер'
        report = 'report', 'Отчетность'


    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.user)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=50, blank=True, unique=True)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.new)
    tg_id = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.'
    )

    USERNAME_FIELD = 'phone_number'
    objects = MyUserManager()

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Manager for User"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in tha system"""
    email = models.EmailField(max_length=255, unique=True,
                              verbose_name='e-mail')
    name = models.CharField(max_length=255, null=True, blank=True,
                            verbose_name='nome')
    cellphone = models.CharField(max_length=14, null=True, blank=True,
                                 verbose_name='telefone')
    is_active = models.BooleanField(default=True, verbose_name='ativo')
    is_staff = models.BooleanField(default=False, verbose_name='funcionário')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def get_full_name(self):
        """get the full name of the user"""
        return self.name

    def get_short_name(self):
        """get only the first name of the user"""
        return self.name.split(' ')[0] if self.name is not None else self.name

    def __str__(self):
        return self.email

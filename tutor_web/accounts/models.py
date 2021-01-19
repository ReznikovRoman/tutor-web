from django.db import models
from django.contrib.auth.models import (User, AbstractUser, BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin, Permission, Group)

from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


#################################################################################################################


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_or_create(self, email, first_name=None, last_name=None, password=None):
        created = True
        try:
            user = self.get(
                email=self.normalize_email(email),
            )
            created = False
        except CustomUser.DoesNotExist:
            user = self.create_user(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.save(using=self._db)

        return user, created


#######################################################################################################################


def get_default_profile_pic():
    return 'images/profile_pics/default_profile_pics/user_1.png'


class CustomUser(AbstractUser, PermissionsMixin):

    # required fields
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    # login parameter
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = CustomUserManager()

    def get_all_permissions(self, obj=None):
        if self.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(group__user=self)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        if perm in self.get_all_permissions() or perm in self.get_group_permissions():
            return True
        return False

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)

    phone_number = PhoneNumberField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile_pics',
                                    default=get_default_profile_pic)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
















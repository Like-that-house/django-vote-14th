from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Candidate(Base):
    name = models.CharField(max_length=50, null=False)
    votes = models.IntegerField(default=0)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, userid, password=None):
        if not "email":
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            userid=userid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, userid, password):
        superuser = self.create_user(
            email=self.normalize_email(email),
            userid=userid,
            password=password)
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, Base):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    userid = models.CharField(max_length=50, unique=True, null=False)
    voteDone = models.BooleanField(default=False)
    voting_for = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voters', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

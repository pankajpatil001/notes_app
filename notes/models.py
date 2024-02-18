from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class NeofiUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class NeofiUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = NeofiUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Note(models.Model):
    owner = models.ForeignKey(NeofiUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username + ' @ ' + str(self.created_at)

class NoteShare(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(NeofiUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' @ ' + str(self.note.updated_at)

class NoteEdit(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(NeofiUser, on_delete=models.CASCADE)
    previous_content = models.TextField()
    edited_content = models.TextField()
    edit_timestamp = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='student'):
        if not email:
            raise ValueError("Email required")
        user = self.model(email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password, role='admin')

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=10)
    access_card_number = models.CharField(max_length=50)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='parents', null=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    access_card_number = models.CharField(max_length=50)
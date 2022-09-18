from turtle import dot
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

# Create your models here.

GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

class UserManager(BaseUserManager):
    def create_user(self, email, name, gender, date_of_birth, caretaker_relation, doctor_name, password=None,cnfm_password=None):
        if not email:
            raise ValueError('Users must have an valid email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            gender=gender,
            date_of_birth=date_of_birth,
            caretaker_relation=caretaker_relation,
            doctor_name=doctor_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, name, gender, date_of_birth, caretaker_relation, doctor_name,password=None):
        user=self.create_user(
            email,
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            caretaker_relation=caretaker_relation,
            doctor_name=doctor_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# class doctor_profile(models.Model):
#     is_doctor = models.

class User(AbstractBaseUser):
    # user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(
            verbose_name = 'Email',
            max_length=100,
            unique=True,
    )
    # password = models.CharField(max_length=100)
    # cnfm_password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)    
    date_of_birth = models.DateField()
    caretaker_relation = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_doctor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','gender','date_of_birth', 'caretaker_relation', 'doctor_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permision"
        #Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permission to view the app"
        #Simple possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    # @property
    # def is_staff(self):
    #     "Is the user a staff?"
    #     return self.is_doctor

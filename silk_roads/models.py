from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom manager for Player model
class custom_userManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class custom_user(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = custom_userManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
def get_default_user():
    user, created = custom_user.objects.get_or_create(username='default', defaults={'email': 'default@example.com'})
    return user.id  # Return the ID of the user instead of the user object
class Stats(models.Model):
    user = models.ForeignKey(custom_user, default=get_default_user, on_delete=models.CASCADE)
    happiness = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    rizz = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    skills = models.IntegerField(default=0)
    esteem = models.IntegerField(default=0)
    moral_compass = models.IntegerField(default=50)
    battery = models.IntegerField(default=100)


class Character(models.Model):
    user = models.ForeignKey(custom_user, on_delete=models.CASCADE, null=True, related_name='characters')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    year = models.IntegerField(default= 2024, help_text=" ")
    gender_choices = [
        ( "Male", "Male"),
        ("Female", "Female")
    ]

    gender = models.CharField(max_length=20, choices=gender_choices)

    ethnicity_choices = [
        ("White", "White"),
        ("Black", "Black"),
        ("European", "European"),
        ("Asian", "Asian"),
        ("Hispanic", "Hispanic"),
        ("Middle Eastern", "Middle Eastern"),
        ("South Asian", "South Asian")
    ]

    ethnicity = models.CharField(max_length=20, choices=ethnicity_choices)
    traits_choices = [
        ('Communicator', 'Communicator'),
        ('Innovator', 'Innovator'),
        ('Motivator', 'Motivator'),
        ('Analyzer', 'Analyzer'),
        ('Networker', 'Networker'),
        ('Mentor', 'Mentor'),
        ('Strategist', 'Strategist'),
        ('Empath', 'Empath'),
        ('Visionary', 'Visionary'),
        ('Activist', 'Activist'),
    ]
    traits = models.CharField(max_length=25, choices=traits_choices)
    background = models.CharField(max_length=250, default= " ")

    TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('Romance', 'Romance'),
        ('Adventure', 'Adventure'),
        ('Success', 'Success'),
        ('Fame', 'Fame'),
        ('Spiritual', 'Spiritual')

    ]
    personality_choices = [
        ('Introvert', 'Introvert'),
        ('Extrovert', 'Extrovert'),
    ]
    type_story = models.CharField(max_length=25, choices=TYPE_CHOICES)
    personality = models.CharField(max_length=20, choices=personality_choices)

def Character_create(name, age, gender,  background, type_story):
    prompt = (f"{name} a {gender}, they are {age} years old, they're background is: ({background}), "
              f"write a short background story for this character by "
              f"crafting a realistic narrative that sets the tone for his {type_story}-oriented story."
              f" Keep it concise, no more than one paragraph.")
    return prompt

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

class Team(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    points = models.IntegerField()
    USERNAME_FIELD = 'name'

    objects = UserManager()


class Players(models.Model):
    ROLES = (
        ('SU','Support'),
        ('JU','Jungle'),
        ('ADC','Attack damage carry'),
        ('MID','Middle'),
        ('SOLO','Solo')
    )
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    top = models.BooleanField()
    role = models.CharField(max_length=4, choices=ROLES, unique=True)
    team = models.ForeignKey(Team, related_name='team')

    def __unicode__(self):
        return self.name

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    class Role(models.TextChoices):
        NONE = 'None'
        MARKETSELLER = 'Market Seller'
        EVENTORGANIZER = 'Event Organizer'
        BOOKCONTRIBUTOR = 'Book Contributor'
        PROJECTCREATOR = 'Project Creator'
        COMMISSIONMAKER = 'Commission Maker'
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    displayName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50,
                            choices=Role.choices,
                            default=Role.NONE)

    def __str__(self):
        return self.displayName

    def get_absolute_url(self):
        return reverse('accounts:profileupdate', kwargs={'displayName': self.displayName})
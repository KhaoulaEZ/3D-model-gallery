from django.db import models

# Create your models here.


class Utilisateur(models.Model):
    Utilisateur_nom = models.CharField(max_length=50)
    Utilisateur_prenom = models.CharField(max_length=50)

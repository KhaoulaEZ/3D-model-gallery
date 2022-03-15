from django.db import models

# Create your models here.
class gallery(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=500, default='name of photo ')  # dans l'affichage
    description = models.CharField(max_length=500, default='description photo ')
    date_pub = models.DateField(null=True,blank=True)
    photo = models.ImageField(upload_to='photos/%y/%m/%d')
    activate = models.BooleanField(default=True)
    pos_x = models.IntegerField(null=True,blank=True)
    pos_y = models.IntegerField(null=True,blank=True)
    width = models.DecimalField(max_digits=3, decimal_places=2,null=True,blank=True)
    heigh = models.DecimalField(max_digits=3, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.nom
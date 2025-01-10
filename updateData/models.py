from django.db import models

# Create your models here.
from django.db import models

class UpdateData(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=10,default='', blank=True)
    website=models.URLField(blank=True, null=True)
    message=models.TextField(max_length=800,default='', blank=True)

    def __str__(self):
        return self.name


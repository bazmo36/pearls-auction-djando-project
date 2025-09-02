from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pearl(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pearls")
    name= models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="pearls/",blank=True, null=True)
    craeted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (owned by {self.owner.username})"
    


class Certification(models.Model):
    pearl = models.OneToOneField(Pearl, on_delete=models.CASCADE, related_name="certification")
    certified_by = models.CharField(max_length=100)
    certificate_number = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=50)
    issued_at = models.DateField()

    def __str__(self):
        return f"Certificate {self.certificate_number} for {self.pearl.name}"
    

    
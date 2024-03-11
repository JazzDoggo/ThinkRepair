from django.contrib.auth.models import User
from django.db import models

# Create your models here.
PART_TYPE_CHOICES = {
    'audio': 'Speakers',
    'battery': 'Battery',
    'camera': 'Webcam',
    'display': 'Display',
    'keyboard': 'Keyboard',
    'memory': 'Memory RAM',
    'motherboard': 'Motherboard',
    'network': 'Network card',
    'storage': 'Hard drive',
    'touch': 'Touchpad',
}


class Laptop(models.Model):
    model = models.CharField(max_length=64, unique=True)
    series = models.CharField(max_length=64)
    manufacturer = models.CharField(max_length=255)
    year = models.IntegerField()


class Part(models.Model):
    product_code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=PART_TYPE_CHOICES, max_length=16)
    details = models.TextField()


# Parts required to build a laptop
class LaptopParts(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='laptop_part')
    alternative = models.ManyToManyField(Part, related_name='alternative_part')


# Laptops belonging to a user
class UserLaptop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    purchased = models.DateTimeField(auto_now_add=True)
    serial = models.CharField(max_length=64, unique=True)


# History of replaced parts for a laptop
class UserReplacedParts(models.Model):
    user_laptop = models.ForeignKey(UserLaptop, on_delete=models.CASCADE)
    part_old = models.ForeignKey(LaptopParts, on_delete=models.CASCADE, null=True)
    # limit options to original part or alternative
    part_current = models.ForeignKey(Part,
                                 # limit_choices_to={'type': part_old.part.type},
                                 on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()

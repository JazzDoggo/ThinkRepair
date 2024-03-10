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
    model = models.CharField(max_length=255, unique=True)
    series = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    year = models.IntegerField()


class Part(models.Model):
    serial = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=PART_TYPE_CHOICES, max_length=16)  # choice
    details = models.TextField()


# Parts required to build a laptop
class LaptopParts(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='laptop_part')  # related_name necessary?
    alternative = models.ManyToManyField(Part, related_name='alternative_part')  # related_name necessary?
    # for each laptop unique part.type?


# Laptops belonging to a user
class UserLaptop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    purchased = models.DateTimeField(auto_now_add=True)


# History of replaced parts for a laptop
class UserReplacedParts(models.Model):
    user_laptop = models.ForeignKey(UserLaptop, on_delete=models.CASCADE)
    # limit_choices_to parts inside the laptop?
    part_old = models.ForeignKey(LaptopParts,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'laptop': user_laptop.laptop})
    # limit options to original part or alternative
    part_new = models.ForeignKey(Part,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'type': part_old.part.type})
    date = models.DateField()
    comment = models.TextField()

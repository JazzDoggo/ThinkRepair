from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f'{self.manufacturer} {self.series} {self.model}'


class Part(models.Model):
    product_code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=PART_TYPE_CHOICES, max_length=16)
    manufacturer = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    def __str__(self):
        return f'{self.manufacturer} {self.name} {self.product_code}'


# Parts required to build a laptop
class LaptopPart(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='laptop_part')
    alternative = models.ManyToManyField(Part, related_name='alternative_part', blank=True)

    def __str__(self):
        return f'{self.part} in {self.laptop}'


@receiver(post_save, sender=LaptopPart)
def create_replaced_part_for_existing(sender, instance, created, *args, **kwargs):
    laptop_part = instance
    user_laptops = laptop_part.laptop.userlaptop_set.all()
    for user_laptop in user_laptops:
        UserReplacedPart.objects.create(user_laptop=user_laptop,
                                        part_original=laptop_part,
                                        part_current=laptop_part.part,
                                        comment='Retail part')


# Laptops belonging to a user
class UserLaptop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    purchased = models.DateField(auto_now_add=True)
    serial = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.laptop} {self.serial}'

    def parts_current(self):
        user_laptop = self
        laptop_parts_current = []
        # if UserReplacedPart.objects.filter(user_laptop=user_laptop).exists():
        for laptop_part in user_laptop.laptop.laptoppart_set.all():
            replaced_parts = UserReplacedPart.objects.filter(user_laptop=user_laptop,
                                                             part_original=laptop_part).order_by('-date')
            laptop_parts_current.append(replaced_parts[0])
        return laptop_parts_current


@receiver(post_save, sender=UserLaptop)
def create_initial_replaced_parts(sender, instance, created, *args, **kwargs):
    laptop_parts = instance.laptop.laptoppart_set.all()
    for laptop_part in laptop_parts:
        UserReplacedPart.objects.create(user_laptop=instance,
                                        part_original=laptop_part,
                                        part_current=laptop_part.part,
                                        comment='Retail part')


# History of replaced parts for a laptop
class UserReplacedPart(models.Model):
    user_laptop = models.ForeignKey(UserLaptop, on_delete=models.CASCADE)
    part_original = models.ForeignKey(LaptopPart, on_delete=models.CASCADE, related_name='replaced_part_original')
    # limit options to original part or alternative
    part_current = models.ForeignKey(Part,
                                     # limit_choices_to={'type': part_old.part.type},
                                     on_delete=models.CASCADE,
                                     related_name='replaced_part_current')
    date = models.DateField(auto_now_add=True)
    comment = models.TextField()

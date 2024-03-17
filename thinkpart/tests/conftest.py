import pytest
from django.contrib.auth.models import User
from django.test import Client
from ThinkRepair import settings

from thinkpart.models import Laptop, Part, LaptopPart, UserLaptop


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def fix_user_data():
    data = {
        'email': 'test@testsite.com',
        'username': 'test',
        'password': 'testpass',
    }
    return data


@pytest.fixture
def fix_user(fix_user_data):
    user = User.objects.create_user(**fix_user_data)
    return user


@pytest.fixture
def fix_user_other():
    data = {
        'email': 'other@othersite.com',
        'username': 'other',
        'password': 'otherpass',
    }
    user = User.objects.create_user(**data)
    return user


@pytest.fixture
def fix_part_data():
    data = {
        'product_code': '12341234',
        'name': 'Test part',
        'type': 'motherboard',
        'manufacturer': 'Lenovo',
        'details': 'abc',
    }
    return data


@pytest.fixture
def fix_parts():
    for i in range(5):
        Part.objects.create(
            product_code=f'{i}' * 8,
            name='Test part',
            type='motherboard',
            manufacturer='Lenovo',
            details='abc',
        )


@pytest.fixture
def fix_laptop_data():
    data = {
        'model': 'X230',
        'series': 'ThinkPad',
        'manufacturer': 'Lenovo',
        'year': 2012
    }
    return data


@pytest.fixture
def fix_laptops():
    for i in range(5):
        Laptop.objects.create(
            model=f'T4{i}0',
            series='ThinkPad',
            manufacturer='Lenovo',
            year=f'201{i}',
        )


@pytest.fixture
def fix_laptop_part_data(fix_parts, fix_laptops):
    part = Part.objects.first()
    alternatives = []
    for p in Part.objects.exclude(pk=part.pk)[:2]:
        alternatives.append(p.pk)
    data = {
        'part': part.pk,
        'alternative': alternatives,
    }
    return data


@pytest.fixture
def fix_laptop_part_data_diff(fix_parts, fix_laptops):
    part = Part.objects.last()
    alternatives = []
    for p in Part.objects.exclude(pk=part.pk)[:2:-1]:
        alternatives.append(p.pk)
    data = {
        'part': part.pk,
        'alternative': alternatives,
    }
    return data


@pytest.fixture
def fix_laptop_parts(fix_parts, fix_laptops):
    part = Part.objects.first()
    laptop = Laptop.objects.first()
    laptop_part = LaptopPart.objects.create(laptop=laptop, part=part)
    for alt in Part.objects.exclude(pk=part.pk)[:2]:
        laptop_part.alternative.add(alt)


@pytest.fixture
def fix_user_laptop_data(fix_laptops):
    laptop = Laptop.objects.first()
    data = {
        'laptop': laptop.pk,
        'serial': 'TEST1234'
    }
    return data


@pytest.fixture
def fix_user_laptop(fix_user, fix_parts, fix_laptops, fix_user_laptop_data):
    laptop = Laptop.objects.get(pk=fix_user_laptop_data['laptop'])
    serial = fix_user_laptop_data['serial']
    UserLaptop.objects.create(laptop=laptop, user=fix_user, serial=serial)

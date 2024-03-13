import pytest
from django.test import Client
from ThinkRepair import settings

from thinkpart.models import Laptop, Part


@pytest.fixture
def client():
    client = Client()
    return client


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
    for i in range(3):
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
    for i in range(3):
        Laptop.objects.create(
            model=f'T4{i}0',
            series='ThinkPad',
            manufacturer='Lenovo',
            year=f'201{i}',
        )

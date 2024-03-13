from random import choice

import pytest
from django.shortcuts import resolve_url
from django.test import TestCase, Client
from django.urls import reverse

from thinkpart.forms import PartForm, LaptopForm
from thinkpart.models import Laptop, Part


# Create your tests here.
def test_home_get(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_part_list_get(client, fix_parts):
    parts = Part.objects.all()
    url = reverse('part_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['parts']) == len(parts)


@pytest.mark.django_db
def test_part_add_get(client):
    url = reverse('part_add')
    response = client.get(url)
    form = response.context['form']
    assert response.status_code == 200
    assert isinstance(form, PartForm)


@pytest.mark.django_db
def test_part_add_post(client, fix_part_data):
    url = reverse('part_add')
    response = client.post(url, fix_part_data)
    assert response.status_code == 302
    assert Part.objects.get(product_code=fix_part_data['product_code'])


@pytest.mark.django_db
def test_part_add_post_invalid(client):
    previous = Part.objects.all()
    url = reverse('part_add')
    response = client.post(url)
    assert response.status_code == 302
    assert len(Part.objects.all()) == len(previous)


@pytest.mark.django_db
def test_part_update_get(client, fix_parts):
    part = Part.objects.first()
    url = resolve_url('part_update', pk=part.pk)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], PartForm)  # better way? compare data?


@pytest.mark.django_db
def test_part_update_post(client, fix_parts, fix_part_data):
    part = Part.objects.first()
    url = resolve_url('part_update', pk=part.pk)
    response = client.post(url, fix_part_data)
    assert response.status_code == 302
    assert fix_part_data['product_code'] == Part.objects.get(pk=part.pk).product_code  # check all fields?


@pytest.mark.django_db
def test_part_detail_get(client, fix_parts):
    part = choice(Part.objects.all())
    url = resolve_url('part_detail', pk=part.pk)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['part'].pk == part.pk


@pytest.mark.django_db
def test_laptop_list_get(client, fix_laptops):
    url = reverse('laptop_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['laptops']) == len(Laptop.objects.all())


@pytest.mark.django_db
def test_laptop_add_get(client):
    url = reverse('laptop_add')
    response = client.get(url)
    form = response.context['form']
    assert response.status_code == 200
    assert isinstance(form, LaptopForm)


@pytest.mark.django_db
def test_laptop_add_post(client, fix_laptop_data):
    url = reverse('laptop_add')
    response = client.post(url, fix_laptop_data)
    assert response.status_code == 302
    assert Laptop.objects.get(model=fix_laptop_data['model'])


@pytest.mark.django_db
def test_laptop_add_post_invalid(client):
    previous = Laptop.objects.all()
    url = reverse('laptop_add')
    response = client.post(url)
    assert response.status_code == 302
    assert len(Laptop.objects.all()) == len(previous)


@pytest.mark.django_db
def test_laptop_detail_get(client, fix_laptops):
    laptop = choice(Laptop.objects.all())
    url = resolve_url('laptop_detail', pk=laptop.pk)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['laptop'].pk == laptop.pk


@pytest.mark.django_db
def test_laptop_update_post(client, fix_laptops, fix_laptop_data):
    laptop = Laptop.objects.first()
    url = resolve_url('laptop_update', pk=laptop.pk)
    response = client.post(url, fix_laptop_data)
    assert response.status_code == 302
    assert fix_laptop_data['model'] == Laptop.objects.get(pk=laptop.pk).model  # check all fields?

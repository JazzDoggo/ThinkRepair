from random import choice

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import ModelFormMetaclass
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


def test_user_register_get(client):
    url = reverse('user_register')
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context['user'].is_authenticated


@pytest.mark.django_db
def test_user_register_post(client, fix_user_data):
    url = reverse('user_register')
    fix_user_data['re_password'] = fix_user_data['password']
    response = client.post(url, fix_user_data)
    assert response.status_code == 302
    assert User.objects.get(username=fix_user_data['username'])


@pytest.mark.django_db
def test_user_register_post_password_diff(client, fix_user_data):
    url = reverse('user_register')
    fix_user_data['re_password'] = 'different'
    response = client.post(url, fix_user_data, follow=True)
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        User.objects.get(username=fix_user_data['username'])


def test_user_login_get(client):
    url = reverse('user_login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login_post(client, fix_user, fix_user_data):
    url = reverse('user_login')
    fix_user_data.pop('email')
    response = client.post(url, fix_user_data, follow=True)
    assert response.status_code == 200
    assert response.context['user'].is_authenticated


@pytest.mark.django_db
def test_user_logout_get(client, fix_user):
    url = reverse('user_logout')
    client.force_login(fix_user)
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert not response.context['user'].is_authenticated


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
def test_part_delete_get(client, fix_parts):
    part = Part.objects.first()
    url = resolve_url('part_delete', pk=part.pk)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_part_delete_get_no_object(client, fix_parts):
    part = Part.objects.last()
    url = resolve_url('laptop_delete', pk=part.pk + 1)
    with pytest.raises(ObjectDoesNotExist):
        response = client.get(url)


@pytest.mark.django_db
def test_part_delete_post(client, fix_parts):
    part = Part.objects.first()
    parts_previous = Part.objects.count()
    url = resolve_url('part_delete', pk=part.pk)
    response = client.post(url, {'confirm': 'True'}, follow=True)
    assert response.status_code == 200
    assert Part.objects.count() == parts_previous - 1


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
    assert isinstance(form, ModelFormMetaclass)


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


@pytest.mark.django_db
def test_laptop_delete_get(client, fix_laptops):
    laptop = Laptop.objects.first()
    url = resolve_url('laptop_delete', pk=laptop.pk)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_laptop_delete_get_no_object(client, fix_laptops):
    laptop = Laptop.objects.last()
    url = resolve_url('laptop_delete', pk=laptop.pk + 1)
    with pytest.raises(ObjectDoesNotExist):
        response = client.get(url)


@pytest.mark.django_db
def test_laptop_delete_post(client, fix_laptops):
    laptop = Laptop.objects.first()
    laptops_previous = Laptop.objects.count()
    url = resolve_url('laptop_delete', pk=laptop.pk)
    response = client.post(url, {'confirm': 'True'}, follow=True)
    assert response.status_code == 200
    assert Laptop.objects.count() == laptops_previous - 1

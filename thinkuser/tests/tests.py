import pytest
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse

from thinkpart.forms import UserLaptopForm, UserReplacedPartForm
from thinkpart.models import UserLaptop, UserReplacedPart
from thinkpart.tests.conftest import *


# Create your tests here.


@pytest.mark.django_db
def test_user_laptop_add_get(client, fix_user):
    client.force_login(user=fix_user)
    url = reverse('user_laptop_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserLaptopForm)


@pytest.mark.django_db
def test_user_laptop_add_get_no_user(client, fix_user):
    url = reverse('user_laptop_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_laptop_add_post(client, fix_user, fix_parts, fix_laptops, fix_laptop_parts, fix_user_laptop_data):
    user_laptops_previous = UserLaptop.objects.count()
    url = reverse('user_laptop_add')
    client.force_login(user=fix_user)
    response = client.post(url, fix_user_laptop_data)
    assert response.status_code == 302
    assert UserLaptop.objects.count() == user_laptops_previous + 1
    user_laptop = UserLaptop.objects.get(user=fix_user)
    laptop_parts = user_laptop.laptop.laptoppart_set.count()
    assert UserReplacedPart.objects.count() == laptop_parts


@pytest.mark.django_db
def test_user_laptop_list_get(client, fix_user, fix_laptops):
    client.force_login(user=fix_user)
    url = reverse('user_laptop_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_laptop_list_get_no_user(client, fix_user, fix_laptops):
    url = reverse('user_laptop_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_laptop_list_get_other_user(client, fix_user_other, fix_laptops):
    url = reverse('user_laptop_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_laptop_current_get(client, fix_user, fix_laptops, fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    url = resolve_url('user_laptop_current', user_laptop.pk)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_laptop_current_get_other_user(client, fix_user, fix_user_other, fix_laptops, fix_user_laptop):
    client.force_login(user=fix_user_other)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    url = resolve_url('user_laptop_current', user_laptop.pk)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_laptop_history_get(client, fix_user, fix_laptops, fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    url = resolve_url('user_laptop_history', user_laptop.pk)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_laptop_history_get_other_user(client, fix_user, fix_user_other, fix_laptops, fix_user_laptop):
    client.force_login(user=fix_user_other)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    url = resolve_url('user_laptop_history', user_laptop.pk)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_laptop_part_delete_get(client, fix_user, fix_parts, fix_laptops, fix_laptop_parts, fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    url = resolve_url('user_laptop_delete', pk=user_laptop.pk)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_laptop_part_delete_post(client, fix_user, fix_parts, fix_laptops, fix_laptop_parts, fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    user_laptop_previous = UserLaptop.objects.count()
    # user_replaced_parts = len(UserReplacedPart.objects.filter(user_laptop=user_laptop))
    # user_replaced_parts_previous = UserReplacedPart.objects.count()
    url = resolve_url('user_laptop_delete', pk=user_laptop.pk)
    response = client.post(url, {'confirm': 'True'}, follow=True)
    assert response.status_code == 200
    assert UserLaptop.objects.count() == user_laptop_previous - 1
    # assert UserReplacedPart.objects.count() == user_replaced_parts_previous - user_replaced_parts
    assert UserReplacedPart.objects.count() == 0


@pytest.mark.django_db
def test_user_replace_part_add_get(client, fix_user, fix_parts, fix_laptops, fix_laptop_parts, fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    laptop_part = user_laptop.laptop.laptoppart_set.first()
    url = resolve_url('user_laptop_replace_part', user_laptop_pk=user_laptop.pk, laptop_part_pk=laptop_part.pk)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserReplacedPartForm)


@pytest.mark.django_db
def test_user_replace_part_add_get_other_user(client, fix_user, fix_user_other, fix_parts, fix_laptops,
                                              fix_laptop_parts, fix_user_laptop):
    client.force_login(user=fix_user_other)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    laptop_part = user_laptop.laptop.laptoppart_set.first()
    url = resolve_url('user_laptop_replace_part', user_laptop_pk=user_laptop.pk, laptop_part_pk=laptop_part.pk)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_replace_part_add_get_diff_laptop(client, fix_user, fix_parts, fix_laptops, fix_laptop_parts,
                                               fix_user_laptop):
    client.force_login(user=fix_user)
    user_laptop = UserLaptop.objects.get(user=fix_user)
    laptop_part = LaptopPart.objects.create(laptop=Laptop.objects.last(), part=Part.objects.first())
    url = resolve_url('user_laptop_replace_part', user_laptop_pk=user_laptop.pk, laptop_part_pk=laptop_part.pk)
    response = client.get(url)
    assert response.status_code == 302

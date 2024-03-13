from django.shortcuts import render, redirect
from django.views import View

from thinkpart.forms import PartForm, LaptopForm, UserRegisterForm
from thinkpart.models import Part, Laptop


# Create your views here.
class HomeView(View):
    def get(self, request):
        response = render(request, 'base.html')
        return response


class UserRegisterView(View):
    def get(self, request):
        cnx = {
            'form_name': 'Register user',
            'form': UserRegisterForm(),
            'form_button': 'Register'
        }
        return render(request, 'form.html', cnx)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect('home')
            return response
        return redirect('user_register')


class PartListView(View):
    def get(self, request):
        parts = Part.objects.all()
        cnx = {'parts': parts}
        response = render(request, 'part_list.html', cnx)
        return response


class PartAddView(View):
    def get(self, request):
        cnx = {
            'form_name': 'Add part',
            'form': PartForm,
            'form_button': 'Add'
        }
        response = render(request, 'form.html', cnx)
        return response

    def post(self, request):
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect('part_list')
            return response
        return redirect('part_add')


class PartDetailView(View):
    def get(self, request, pk):
        part = Part.objects.get(pk=pk)
        response = render(request, 'part_detail.html', {'part': part})
        return response


class PartUpdateView(View):
    def get(self, request, pk):
        part = Part.objects.get(pk=pk)
        cnx = {
            'form_name': f'Update {part}',
            'form': PartForm(instance=part),
            'form_button': 'Update'
        }
        return render(request, 'form.html', cnx)

    def post(self, request, pk):
        part = Part.objects.get(pk=pk)
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('part_list')
        return redirect('part_update', pk=part.pk)


class LaptopListView(View):
    def get(self, request):
        laptops = Laptop.objects.all()
        cnx = {'laptops': laptops}
        response = render(request, 'laptop_list.html', cnx)
        return response


class LaptopAddView(View):
    def get(self, request):
        cnx = {
            'form_name': 'Add laptop',
            'form': LaptopForm,
            'form_button': 'Add'
        }
        response = render(request, 'form.html', cnx)
        return response

    def post(self, request):
        form = LaptopForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect('laptop_list')
            return response
        return redirect('laptop_add')


class LaptopDetailView(View):
    def get(self, request, pk):
        laptop = Laptop.objects.get(pk=pk)
        response = render(request, 'laptop_detail.html', {'laptop': laptop})
        return response


class LaptopUpdateView(View):
    def get(self, request, pk):
        laptop = Laptop.objects.get(pk=pk)
        cnx = {
            'form_name': f'Update {laptop}',
            'form': LaptopForm(instance=laptop),
            'form_button': 'Update'
        }
        return render(request, 'form.html', cnx)

    def post(self, request, pk):
        laptop = Laptop.objects.get(pk=pk)
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('laptop_list')
        return redirect('laptop_update', pk=laptop.pk)

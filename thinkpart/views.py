from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from thinkpart.forms import PartForm, LaptopForm, UserRegisterForm, UserLoginForm, LaptopPartForm
from thinkpart.models import Part, Laptop, LaptopPart


# Create your views here.
class HomeView(View):
    def get(self, request):
        response = render(request, 'base.html')
        return response


# USER VIEWS


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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_login')
        return redirect('user_register')


class UserLoginView(View):
    def get(self, request):
        cnx = {
            'form_name': 'Login',
            'form': UserLoginForm(),
            'form_button': 'Login'
        }
        return render(request, 'form.html', cnx)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
        return redirect('user_login')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        response = redirect('home')
        return response


# PARTS VIEWS


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
            'form': PartForm(),
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


class PartDeleteView(View):
    def get(self, request, pk):
        part = Part.objects.get(pk=pk)
        response = render(request, 'form_delete.html', {'object': part})
        return response

    def post(self, request, pk):
        part = Part.objects.get(pk=pk)
        if request.POST.get('confirm') == 'True':
            part.delete()
        return redirect('part_list')


# LAPTOP VIEWS


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
            'form': LaptopForm(),
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


class LaptopDeleteView(View):
    def get(self, request, pk):
        laptop = Laptop.objects.get(pk=pk)
        response = render(request, 'form_delete.html', {'object': laptop})
        return response

    def post(self, request, pk):
        laptop = Laptop.objects.get(pk=pk)
        if request.POST.get('confirm') == 'True':
            laptop.delete()
        return redirect('laptop_list')


# LAPTOP PARTS VIEWS


class LaptopPartAddView(View):
    def get(self, request, laptop_pk):
        laptop = Laptop.objects.get(pk=laptop_pk)
        cnx = {
            'form_name': f'Add laptop part to {laptop}',
            'form': LaptopPartForm(),
            'form_button': 'Add'
        }
        return render(request, 'form.html', cnx)

    def post(self, request, laptop_pk):
        laptop = Laptop.objects.get(pk=laptop_pk)
        form = LaptopPartForm(request.POST)
        if form.is_valid():
            laptop_part = form.save(commit=False)
            laptop_part.laptop = laptop
            laptop_part.save()
            laptop_part.alternative.set(form.cleaned_data['alternative'])
        return redirect('laptop_detail', laptop.pk)


class LaptopPartUpdateView(View):
    def get(self, request, laptop_pk, laptop_part_pk):
        laptop = Laptop.objects.get(pk=laptop_pk)
        laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
        cnx = {
            'form_name': f'Update laptop part for {laptop}',
            'form': LaptopPartForm(instance=laptop_part),
            'form_button': 'Update'
        }
        return render(request, 'form.html', cnx)

    def post(self, request, laptop_pk, laptop_part_pk):
        laptop = Laptop.objects.get(pk=laptop_pk)
        laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
        form = LaptopPartForm(request.POST, instance=laptop_part)
        if form.is_valid():
            laptop_part = form.save(commit=False)
            laptop_part.laptop = laptop
            laptop_part.save()
            laptop_part.alternative.set(form.cleaned_data['alternative'], clear=True)
        return redirect('laptop_detail', laptop.pk)


class LaptopPartDeleteView(View):
    def get(self, request, laptop_pk, laptop_part_pk):
        laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
        return render(request, 'form_delete.html', {'object': laptop_part})

    def post(self, request, laptop_pk, laptop_part_pk):
        if request.POST.get('confirm') == 'True':
            laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
            laptop_part.clean()
            laptop_part.delete()
        return redirect('laptop_detail', laptop_pk)

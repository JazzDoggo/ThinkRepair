from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View

from thinkpart.forms import UserLaptopForm, UserReplacedPartForm
from thinkpart.models import UserLaptop, UserReplacedPart, LaptopPart


# Create your views here.
class UserLaptopAddView(LoginRequiredMixin, View):
    def get(self, request):
        cnx = {
            'form_name': f'Add laptop to your account',
            'form': UserLaptopForm(),
            'form_button': 'Add'
        }
        return render(request, 'form.html', cnx)

    def post(self, request):
        user = request.user
        form = UserLaptopForm(request.POST)
        if form.is_valid():
            user_laptop = form.save(commit=False)
            user_laptop.user = user
            form.save()
            # laptop_parts = user_laptop.laptop.laptoppart_set.all()
            # for laptop_part in laptop_parts:
            #     UserReplacedPart.objects.create(user_laptop=user_laptop,
            #                                     part_original=laptop_part,
            #                                     part_current=laptop_part.part,
            #                                     comment='Retail part')
        return redirect('user_laptop_list')


class UserLaptopListView(LoginRequiredMixin, View):
    def get(self, request):
        user_laptops = UserLaptop.objects.filter(user=request.user)
        cnx = {
            'laptops': user_laptops
        }
        return render(request, 'user_laptop_list.html', cnx)


class UserLaptopDetailCurrentView(UserPassesTestMixin, View):
    def test_func(self):
        user_current = self.request.user
        user_laptop = UserLaptop.objects.get(pk=self.kwargs['pk'])
        return user_current == user_laptop.user

    def get(self, request, pk):
        user_laptop = UserLaptop.objects.get(pk=pk)
        cnx = {
            'user_laptop': user_laptop,
            'user_laptop_replaced_parts': user_laptop.parts_current()
        }
        return render(request, 'user_laptop_current.html', cnx)


class UserLaptopDetailHistoryView(UserPassesTestMixin, View):
    def test_func(self):
        user_current = self.request.user
        user_laptop = UserLaptop.objects.get(pk=self.kwargs['pk'])
        return user_current == user_laptop.user

    def get(self, request, pk):
        user_laptop = UserLaptop.objects.get(pk=pk)
        cnx = {
            'user_laptop': user_laptop,
            'user_laptop_replaced_parts': user_laptop.userreplacedpart_set.all()
        }
        return render(request, 'user_laptop_history.html', cnx)


class UserLaptopDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        user_current = self.request.user
        user_laptop = UserLaptop.objects.get(pk=self.kwargs['pk'])
        return user_current == user_laptop.user

    def get(self, request, pk):
        user_laptop = UserLaptop.objects.get(pk=pk)
        return render(request, 'form_delete.html', {'object': user_laptop})

    def post(self, request, pk):
        if request.POST.get('confirm') == 'True':
            user_laptop = UserLaptop.objects.get(pk=pk)
            user_laptop.clean()
            user_laptop.delete()
        return redirect('user_laptop_list')


class UserReplacedPartAddView(UserPassesTestMixin, View):
    def test_func(self):
        user_current = self.request.user
        user_laptop = UserLaptop.objects.get(pk=self.kwargs['user_laptop_pk'])
        return user_current == user_laptop.user

    def get(self, request, user_laptop_pk, laptop_part_pk):
        user_laptop = UserLaptop.objects.get(pk=user_laptop_pk)
        laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
        if not UserReplacedPart.objects.filter(user_laptop=user_laptop,
                                               part_original=laptop_part).exists():
            return redirect('user_laptop_current', pk=user_laptop_pk)
        cnx = {
            'form_name': f'Replace {laptop_part.part} in {user_laptop}',
            'form': UserReplacedPartForm(laptop_part=laptop_part),
            'form_button': 'Replace'
        }
        return render(request, 'form.html', cnx)

    def post(self, request, user_laptop_pk, laptop_part_pk):
        user_laptop = UserLaptop.objects.get(pk=user_laptop_pk)
        laptop_part = LaptopPart.objects.get(pk=laptop_part_pk)
        if UserReplacedPart.objects.filter(user_laptop=user_laptop, part_original=laptop_part).exists():
            form = UserReplacedPartForm(request.POST)
            if form.is_valid():
                user_replaced_part = form.save(commit=False)
                user_replaced_part.user_laptop = user_laptop
                user_replaced_part.part_original = laptop_part
                user_replaced_part.save()
        return redirect('user_laptop_current', pk=user_laptop_pk)

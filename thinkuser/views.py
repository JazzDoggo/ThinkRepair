from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View

from thinkpart.forms import UserLaptopForm
from thinkpart.models import UserLaptop, UserReplacedPart


def userlaptop_parts_current(pk):
    user_laptop = UserLaptop.objects.get(pk=pk)
    laptop_parts_current = []
    # if UserReplacedPart.objects.filter(user_laptop=user_laptop).exists():
    for laptop_part in user_laptop.laptop.laptoppart_set.all():
        laptop_parts = UserReplacedPart.objects.filter(user_laptop=user_laptop,
                                                       part_original=laptop_part).order_by('-date')
        laptop_parts_current.append(laptop_parts[0])
    return laptop_parts_current


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


class UserLaptopDetailView(UserPassesTestMixin, View):
    def test_func(self):
        user_current = self.request.user
        user_laptop = UserLaptop.objects.get(pk=self.kwargs['pk'])
        return user_current == user_laptop.user

    def get(self, request, pk):
        user_laptop = UserLaptop.objects.get(pk=pk)
        cnx = {
            'user_laptop': user_laptop,
            'user_laptop_parts_current': userlaptop_parts_current(pk)
        }
        return render(request, 'user_laptop_detail.html', cnx)


class UserLaptopDeleteView(LoginRequiredMixin, View):
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

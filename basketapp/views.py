from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView

from basketapp.models import Basket
from mainapp.models import Product


class BasketView(LoginRequiredMixin, ListView):
    model = Basket
    template_name = 'basketapp/basket.html'
    extra_context = {'title': 'Корзина'}

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


# @login_required
# def basket(request):
#     title = 'корзина'
#     basket_items = Basket.objects.filter(user=request.user)
#
#     context = {
#         'title': title,
#         'basket_items': basket_items,
#     }
#
#     return render(request, 'basketapp/basket.html', context)


class BasketAddView(LoginRequiredMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        if 'login' in self.request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('products:product', kwargs={'pk': self.kwargs['pk']}))

        product_item = get_object_or_404(Product, pk=self.kwargs['pk'])
        basket_item = Basket.objects.filter(product=product_item, user=self.request.user).first()

        if not basket_item:
            basket_item = Basket(product=product_item, user=self.request.user)

        basket_item.quantity += 1
        basket_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def basket_add(request, pk):
#     if 'login' in request.META.get('HTTP_REFERER'):
#         return HttpResponseRedirect(reverse('products:product', args=[pk]))
#
#     product_item = get_object_or_404(Product, pk=pk)
#
#     basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
#
#     if not basket_item:
#         basket_item = Basket(product=product_item, user=request.user)
#
#     basket_item.quantity += 1
#     basket_item.save()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketRemoveView(LoginRequiredMixin, DeleteView):

    model = Basket
    template_name = 'basketapp/basket_check_delete.html'
    success_url = reverse_lazy('basket:basket')


# @login_required
# def basket_remove(request, pk):
#     basket_item = get_object_or_404(Basket, pk=pk)
#     basket_item.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user)

        context = {
            'basket_list': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})

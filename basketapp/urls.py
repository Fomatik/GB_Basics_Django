from django.urls import path

from basketapp import views as basket


app_name = 'basketapp'


urlpatterns = [
    path('', basket.basket, name='basket'),
    path('add/<int:pk>/', basket.basket_add, name='add'),
    path('remove/<int:pk>/', basket.basket_remove, name='remove'),
]
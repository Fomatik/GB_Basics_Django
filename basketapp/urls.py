from django.urls import path

from basketapp import views as basket

app_name = 'basketapp'

urlpatterns = [
    path('', basket.BasketView.as_view(), name='basket'),
    path('add/<int:pk>/', basket.BasketAddView.as_view(), name='add'),
    path('remove/<int:pk>/', basket.BasketRemoveView.as_view(), name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basket.basket_edit, name='edit')
]

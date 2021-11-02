from django.urls import path

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.ProductsView.as_view(), name='products'),
    path('category/<int:pk>/', mainapp.ProductsFromCategoryView.as_view(), name='category'),
    path('category/<int:pk>/<int:page>/', mainapp.ProductsFromCategoryView.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductView.as_view(), name='product'),
]

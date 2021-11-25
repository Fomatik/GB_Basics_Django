import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.AdminUserCreateView.as_view(), name='user_create'),
    path('users/read/', adminapp.AdminUserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', adminapp.AdminUserEditView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.AdminUserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.AdminCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.AdminCategoriesView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', adminapp.AdminCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.AdminCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', adminapp.AdminProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.AdminCategoryProductsView.as_view(), name='products'),
    path('products/read/<int:pk>/', adminapp.AdminProductView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', adminapp.AdminProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.AdminProductDeleteView.as_view(), name='product_delete'),
]
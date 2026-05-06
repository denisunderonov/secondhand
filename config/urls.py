
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('category/<int:pk>/products/', views.cat_category, name='cat_category'),
]

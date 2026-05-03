
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
]

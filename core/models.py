from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.db.models import Count

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class CategoryManager(models.Manager): # Собственный модельный менеджер
    def get_products_count(self):
        return self.get_queryset().annotate(product_count=Count("products"))
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    objects = CategoryManager()

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Размеры"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Теги"
        verbose_name_plural = "Теги"
        
    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_new_products(self):
        return self.get_queryset().filter(
            created_at__gte=timezone.now() - timedelta(days=7),
        ).order_by("-created_at")[:3] 

    def get_most_cheap_products(self):
        return self.get_queryset().exclude(price__gt=2000).order_by("price")[:3]


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="+") 
    price = models.FloatField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="products")
    condition = models.CharField(max_length=100, choices=[("new", "Новый"), ("used", "Б/У")])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk}) #kwargs позволяет передать параметры в url

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        
        
    def __str__(self):
        return self.name
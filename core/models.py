from django.db import models

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

class Category(models.Model):
    name = models.CharField(max_length=100)
    
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

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    description = models.TextField()
    price = models.FloatField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        
        
 
    def __str__(self):
        return self.name


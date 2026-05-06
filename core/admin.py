from django.contrib import admin

from . import models


class ProductCategoryInline(admin.TabularInline):
    model = models.Product
    extra = 0


class ProductBrandInline(admin.TabularInline):
    model = models.Product
    extra = 0


class ProductSizeInline(admin.TabularInline):
    model = models.Product
    extra = 0


class ProductTagInline(admin.TabularInline):
    model = models.Product.tags.through
    extra = 0


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("name", "email") # метод list_display_links позволяет кликнуть на имя или email пользователя для редактирования
    

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = [ # inline позволяет добавлять товары в категорию через админку
        ProductCategoryInline
    ]


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    inlines = [
        ProductBrandInline
    ]


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
    inlines = [
        ProductSizeInline
    ]


@admin.register(models.Product) 
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price_display", "brand", "category", "size", "tags_display", "created_at")
    search_fields = ("name", "description", "brand__name", "tags__name")
    list_filter = ("category", "size", "brand", "tags", "created_at") # метод list_filter позволяет фильтровать список товаров по выбранным полям
    date_hierarchy = "created_at" # метод date_hierarchy позволяет просматривать товары по дате создания
    filter_horizontal = ("tags",) # метод filter_horizontal позволяет выбрать теги для товара через админку
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("brand", "category", "size") # метод raw_id_fields 

    def price_display(self, obj): 
        return f"{obj.price} руб."
    price_display.short_description = "Цена"

    def tags_display(self, obj):
        return ", ".join(obj.tags.values_list("name", flat=True))
    tags_display.short_description = "Теги"

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = [
        ProductTagInline
    ]

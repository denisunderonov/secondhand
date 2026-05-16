from django.contrib import admin
from django.db.models import Avg, Sum
from django.utils.translation import gettext_lazy as _

from . import models
from .generatepdf import pdf_response_from_template


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
    change_list_template = "admin/core/product/change_list.html"
    actions = ["export_products_pdf"]
    list_display = ("name", "price_display", "brand", "category", "size", "tags_display", "created_at")
    search_fields = ("name", "description", "brand__name", "tags__name")
    list_filter = ("category", "size", "brand", "tags", "created_at") # метод list_filter позволяет фильтровать список товаров по выбранным полям
    date_hierarchy = "created_at" # метод date_hierarchy позволяет просматривать товары по дате создания
    filter_horizontal = ("tags",) # метод filter_horizontal позволяет выбрать теги для товара через админку
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("brand", "category", "size") # метод raw_id_fields 

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {} # extra_context позволяет передать данные в шаблон
        extra_context["catalog_price_aggregate"] = models.Product.objects.aggregate( # aggregate позволяет получить статистику по товарам
            avg_price=Avg("price"),
            sum_prices=Sum("price"),
        )
        return super().changelist_view(request, extra_context=extra_context) # super() позволяет вызвать метод родителя

    def price_display(self, obj): 
        return f"{obj.price} руб."
    price_display.short_description = "Цена"

    def tags_display(self, obj):
        return ", ".join(obj.tags.values_list("name", flat=True)) # values_list("name", flat=True) позволяет получить список тегов в виде строки
    tags_display.short_description = "Теги"

    @admin.action(description=_("Скачать выбранные товары в PDF")) # action позволяет добавить действие в админку
    def export_products_pdf(self, request, queryset):
        queryset = queryset.select_related("brand", "category", "size").prefetch_related("tags").order_by("pk") 
        return pdf_response_from_template( # функция для генерации PDF отчета о товарах
            "core/pdf/products_report.html",
            {"products": queryset}, # контекст для шаблона
            filename="products.pdf", # имя файла для скачивания
        )


@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ("product", "tag", "assigned_at")
    list_filter = ("tag",)
    autocomplete_fields = ("product", "tag")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    inlines = [
        ProductTagInline
    ]

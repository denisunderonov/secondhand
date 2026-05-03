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
    list_display_links = ("name", "email")
    

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = [
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
    list_filter = ("category", "size", "brand", "tags", "created_at")
    date_hierarchy = "created_at"
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("brand", "category", "size")

    @admin.display(description="Цена")
    def price_display(self, obj):
        return f"{obj.price} руб."

    @admin.display(description="Теги")
    def tags_display(self, obj):
        return ", ".join(obj.tags.values_list("name", flat=True))

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = [
        ProductTagInline
    ]

from django.contrib import admin

from . import models


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


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price_display", "brand", "category", "size", "created_at")
    search_fields = ("name", "description", "brand__name")
    list_filter = ("category", "size", "brand", "created_at")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("brand", "category", "size")

    @admin.display(description="Цена")
    def price_display(self, obj):
        return f"{obj.price} руб."


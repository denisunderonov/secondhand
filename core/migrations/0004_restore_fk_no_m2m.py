# Переход Product: убрано M2M brands, добавлены FK brand/category/size и промежуточные модели.

import django.db.models.deletion
from django.db import migrations, models


def forwards_fill_product_fks(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    ProductBrand = apps.get_model("core", "ProductBrand")
    Brand = apps.get_model("core", "Brand")
    Category = apps.get_model("core", "Category")
    Size = apps.get_model("core", "Size")

    cat, _ = Category.objects.get_or_create(name="Без категории")
    sz, _ = Size.objects.get_or_create(name="Универсальный")

    fallback_brand = Brand.objects.order_by("pk").first()

    for p in Product.objects.all():
        pb = ProductBrand.objects.filter(product_id=p.pk).order_by("pk").first()
        brand_id = pb.brand_id if pb else (fallback_brand.pk if fallback_brand else None)
        if brand_id is None:
            b = Brand.objects.create(name=f"Brand for product {p.pk}")
            brand_id = b.pk
        p.brand_id = brand_id
        p.category_id = cat.pk
        p.size_id = sz.pk
        p.save(update_fields=["brand_id", "category_id", "size_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_product_brands_only"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="product",
            name="brands",
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.brand",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.category",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.size",
            ),
        ),
        migrations.RunPython(forwards_fill_product_fks, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.brand",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.category",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="size",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.size",
            ),
        ),
        migrations.CreateModel(
            name="ProductSize",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.product",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.size",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.category",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.product",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="productsize",
            constraint=models.UniqueConstraint(
                fields=("product", "size"),
                name="uniq_core_productsize_product_size",
            ),
        ),
        migrations.AddConstraint(
            model_name="productcategory",
            constraint=models.UniqueConstraint(
                fields=("product", "category"),
                name="uniq_core_productcategory_product_category",
            ),
        ),
    ]

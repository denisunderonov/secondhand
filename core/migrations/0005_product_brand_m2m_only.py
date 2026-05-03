from django.db import migrations, models


def forwards_productbrand_from_fk(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    ProductBrand = apps.get_model("core", "ProductBrand")
    for p in Product.objects.all():
        bid = getattr(p, "brand_id", None)
        if bid:
            ProductBrand.objects.get_or_create(
                product_id=p.pk,
                brand_id=bid,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_restore_fk_no_m2m"),
    ]

    operations = [
        migrations.RunPython(forwards_productbrand_from_fk, migrations.RunPython.noop),
        migrations.AddField(
            model_name="product",
            name="brands",
            field=models.ManyToManyField(
                blank=True,
                related_name="+",
                through="core.ProductBrand",
                to="core.brand",
            ),
        ),
        migrations.RemoveField(
            model_name="product",
            name="brand",
        ),
    ]

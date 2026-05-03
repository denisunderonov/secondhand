import django.db.models.deletion
from django.db import migrations, models


def forwards_brand_from_junction_or_default(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    ProductBrand = apps.get_model("core", "ProductBrand")
    Brand = apps.get_model("core", "Brand")
    fb = Brand.objects.order_by("pk").first()
    if fb is None:
        fb = Brand.objects.create(name="Не указано")
    for p in Product.objects.all():
        pb = ProductBrand.objects.filter(product_id=p.pk).order_by("pk").first()
        p.brand_id = pb.brand_id if pb else fb.pk
        p.save(update_fields=["brand_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_drop_redundant_junctions"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.brand",
            ),
        ),
        migrations.RunPython(
            forwards_brand_from_junction_or_default,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="product",
            name="brands",
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.brand",
            ),
        ),
        migrations.DeleteModel(
            name="ProductBrand",
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_product_is_featured"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="gender",
            field=models.CharField(
                choices=[("hombre", "Hombre"), ("mujer", "Mujer")],
                default="hombre",
                max_length=10,
                verbose_name="Género",
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_seed_sizes_colors"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_featured",
            field=models.BooleanField(
                default=False,
                help_text="Marcar para mostrar en la sección de Productos Destacados del Inicio",
                verbose_name="Destacado",
            ),
        ),
    ]

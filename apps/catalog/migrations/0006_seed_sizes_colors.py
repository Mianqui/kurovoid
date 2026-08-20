from django.db import migrations


def crear_tallas_y_colores(apps, schema_editor):
    Size = apps.get_model("catalog", "Size")
    Color = apps.get_model("catalog", "Color")

    for name in ["XS", "S", "M", "L", "XL", "XXL"]:
        Size.objects.get_or_create(name=name)

    colores = [
        ("Negro", "#000000"),
        ("Blanco", "#FFFFFF"),
        ("Gris", "#808080"),
        ("Rojo", "#E53935"),
        ("Azul", "#1E88E5"),
        ("Verde", "#43A047"),
        ("Amarillo", "#FDD835"),
        ("Rosa", "#EC407A"),
        ("Morado", "#8E24AA"),
        ("Naranja", "#FB8C00"),
        ("Beige", "#D7CCC8"),
        ("Cafe", "#6D4C41"),
    ]
    for name, hex_code in colores:
        Color.objects.get_or_create(name=name, defaults={"hex_code": hex_code})


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_product_category"),
    ]

    operations = [
        migrations.RunPython(crear_tallas_y_colores, migrations.RunPython.noop),
    ]

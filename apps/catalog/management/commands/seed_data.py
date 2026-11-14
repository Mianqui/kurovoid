import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from catalog.models import Category, Color, Product, ProductImage, Size

PRODUCTS = [
    {"name": "Camiseta Void Negra", "desc": "Camiseta de algodón premium con logo bordado.", "price": 45000, "sizes": "XS,S,M,L,XL", "colors": "Negro,Gris"},
    {"name": "Camiseta Void Blanca", "desc": "Camiseta básica de corte relajado.", "price": 42000, "sizes": "S,M,L,XL", "colors": "Blanco,Negro"},
    {"name": "Buzo Kurovoid", "desc": "Buzo con capucha y bolsillo canguro.", "price": 89000, "sizes": "S,M,L,XL", "colors": "Negro,Gris Oscuro"},
    {"name": "Jeans Ajustados", "desc": "Jeans de mezclilla elástica.", "price": 79000, "sizes": "28,30,32,34,36", "colors": "Azul,Negro"},
    {"name": "Joggers Urbanos", "desc": "Joggers de tela oxford con puños elastizados.", "price": 65000, "sizes": "S,M,L,XL", "colors": "Negro,Gris"},
    {"name": "Chaqueta Rider", "desc": "Chaqueta de poliéster con cierre metálico.", "price": 120000, "sizes": "M,L,XL", "colors": "Negro"},
    {"name": "Gorra KUROVOID", "desc": "Gorra ajustable con logo frontal.", "price": 25000, "sizes": "Única", "colors": "Negro,Blanco,Rojo"},
    {"name": "Medias Premium", "desc": "Par de medias largas con diseño KUROVOID.", "price": 12000, "sizes": "Única", "colors": "Negro,Blanco"},
    {"name": "Camisa Oversize", "desc": "Camisa de corte oversized en algodón.", "price": 55000, "sizes": "M,L,XL", "colors": "Blanco,Negro,Azul"},
    {"name": "Short Deportivo", "desc": "Short de tela dry-fit para entrenamiento.", "price": 35000, "sizes": "S,M,L,XL", "colors": "Negro,Gris,Rojo"},
]

COLORS = [
    ("Negro", "#000000"), ("Blanco", "#FFFFFF"), ("Gris", "#808080"),
    ("Gris Oscuro", "#404040"), ("Azul", "#0000FF"), ("Rojo", "#FF0000"),
]

SIZES = ["XS", "S", "M", "L", "XL", "28", "30", "32", "34", "36", "Única"]


class Command(BaseCommand):
    help = "Llena la BD con datos de prueba"

    def handle(self, *args, **options):
        self.stdout.write("Poblando base de datos...")

        cat_hombre, _ = Category.objects.get_or_create(
            name="Hombre", defaults={"description": "Ropa y accesorios para hombre"}
        )
        cat_mujer, _ = Category.objects.get_or_create(
            name="Mujer", defaults={"description": "Ropa y accesorios para mujer"}
        )
        cat_accesorios, _ = Category.objects.get_or_create(
            name="Accesorios", defaults={"description": "Gorras, medias y más"}
        )

        size_objs = {}
        for name in SIZES:
            s, _ = Size.objects.get_or_create(name=name)
            size_objs[name] = s

        color_objs = {}
        for name, hexcode in COLORS:
            c, _ = Color.objects.get_or_create(name=name, defaults={"hex_code": hexcode})
            color_objs[name] = c

        cat_map = {
            "Camiseta": cat_hombre, "Buzo": cat_hombre, "Jeans": cat_hombre,
            "Joggers": cat_hombre, "Chaqueta": cat_hombre, "Camisa": cat_hombre,
            "Short": cat_hombre, "Gorra": cat_accesorios, "Medias": cat_accesorios,
        }

        for pd in PRODUCTS:
            first_word = pd["name"].split()[0]
            cat = cat_map.get(first_word, cat_hombre)
            product, created = Product.objects.get_or_create(
                name=pd["name"],
                defaults={
                    "category": cat,
                    "description": pd["desc"],
                    "price": pd["price"],
                    "stock": 10,
                    "is_active": True,
                },
            )
            for sn in pd["sizes"].split(","):
                if sn.strip() in size_objs:
                    product.sizes.add(size_objs[sn.strip()])
            for cn in pd["colors"].split(","):
                if cn.strip() in color_objs:
                    product.colors.add(color_objs[cn.strip()])
            if created:
                self.stdout.write(f"  + {pd['name']}")

        user, created = User.objects.get_or_create(
            username="cliente",
            defaults={
                "first_name": "Cliente",
                "last_name": "Kurovoid",
                "email": "cliente@kurovoid.com",
            },
        )
        if created:
            password = os.environ.get("SEED_CLIENT_PASSWORD")
            if password:
                user.set_password(password)
                user.save(update_fields=["password"])
                self.stdout.write(
                    "  + Usuario 'cliente' creado con la contraseña de SEED_CLIENT_PASSWORD."
                )
            else:
                user.set_unusable_password()
                user.save(update_fields=["password"])
                self.stdout.write(
                    self.style.WARNING(
                        "  + Usuario 'cliente' creado sin contraseña de acceso. "
                        "Define SEED_CLIENT_PASSWORD o usa "
                        "'python manage.py changepassword cliente'."
                    )
                )

        self.stdout.write(self.style.SUCCESS("¡BD poblada exitosamente!"))

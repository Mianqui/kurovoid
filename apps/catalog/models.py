from django.db import models
from django.utils.text import slugify


# Tallas disponibles (XS, S, M, L, XL)
class Size(models.Model):
    name = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


# Colores con código hexadecimal
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


# Categoría de productos
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["orden", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Producto individual
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    GENDER_CHOICES = [
        ("hombre", "Hombre"),
        ("mujer", "Mujer"),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="hombre",
        verbose_name="Género",
    )
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Destacado",
        help_text="Marcar para mostrar en la sección de Productos Destacados del Inicio",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def nivel_stock(self):
        if self.stock == 0:
            return "agotado"
        if self.stock <= 3:
            return "bajo"
        return "ok"

    def main_image(self):
        if hasattr(self, "_main_images") and self._main_images:
            return self._main_images[0]
        main = self.images.filter(is_main=True).first()
        if main:
            return main
        return self.images.first()

    def __str__(self):
        return self.name


# Imágenes asociadas a un producto
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="productos/galeria/")
    is_main = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True, null=True, help_text="Opcional: enlace al hacer click")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Carrusel Imagen {self.id}"

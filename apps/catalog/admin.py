from django.contrib import admin

from .models import Category, Color, InstagramPost, Product, ProductImage, Size


# Permite subir imágenes desde el formulario del producto
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "category", "price", "stock", "is_active", "created_at")
    list_filter = ("category", "is_active", "sizes", "colors")
    search_fields = ("name", "description")
    filter_horizontal = ("sizes", "colors")
    inlines = [ProductImageInline]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ("__str__", "orden", "is_active", "created_at")
    list_editable = ("orden", "is_active")
    list_filter = ("is_active",)

from django import forms
from django.utils.text import slugify

from catalog.models import Category, Color, Product, ProductImage, Size

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 text-white rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-white transition-colors"
SELECT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-white transition-colors"
TEXTAREA_CLASSES = "w-full bg-zinc-800 border border-zinc-700 text-white rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-white transition-colors"
CHECKBOX_CLASSES = "w-4 h-4 rounded border-zinc-600 bg-zinc-700 text-white focus:ring-white focus:ring-offset-0 cursor-pointer"


class ProductForm(forms.ModelForm):
    sizes_text = forms.CharField(
        required=False,
        label="Tallas (separadas por coma)",
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Ej: S, M, L, XL"}),
    )
    colors_text = forms.CharField(
        required=False,
        label="Colores (separados por coma)",
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Ej: Rojo, Azul, Negro"}),
    )
    image = forms.ImageField(required=False, label="Imagen principal")

    class Meta:
        model = Product
        fields = [
            "name", "category", "description", "price",
            "stock", "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Nombre del producto"}),
            "category": forms.Select(attrs={"class": SELECT_CLASSES}),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASSES, "rows": 4, "placeholder": "Descripción del producto..."}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "0.00"}),
            "stock": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["sizes_text"].initial = ", ".join(
                [s.name for s in self.instance.sizes.all()]
            )
            self.fields["colors_text"].initial = ", ".join(
                [c.name for c in self.instance.colors.all()]
            )

    def save(self, commit=True):
        product = super().save(commit=False)
        if not product.slug:
            product.slug = slugify(product.name)
        if commit:
            product.save()
            self.save_m2m()

            sizes_input = self.cleaned_data.get("sizes_text", "")
            size_names = [s.strip() for s in sizes_input.split(",") if s.strip()]
            size_objs = []
            for name in size_names:
                obj, _ = Size.objects.get_or_create(name=name.upper())
                size_objs.append(obj)
            product.sizes.set(size_objs)

            colors_input = self.cleaned_data.get("colors_text", "")
            color_names = [c.strip() for c in colors_input.split(",") if c.strip()]
            color_objs = []
            for name in color_names:
                name = name.capitalize()
                obj, _ = Color.objects.get_or_create(name=name, defaults={"hex_code": "#000000"})
                color_objs.append(obj)
            product.colors.set(color_objs)

            image = self.cleaned_data.get("image")
            if image:
                ProductImage.objects.update_or_create(
                    product=product, is_main=True,
                    defaults={"image": image, "alt_text": product.name},
                )
        return product

from django import forms
from django.utils.text import slugify

from catalog.models import Category, Color, Product, ProductImage, Size

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"
SELECT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-accent transition-colors"
TEXTAREA_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"
CHECKBOX_CLASSES = "w-4 h-4 rounded border-zinc-600 bg-zinc-700 theme-text-primary focus:ring-accent focus:ring-offset-0 cursor-pointer"


class ProductForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    image = forms.ImageField(required=False, label="Imagen principal")

    class Meta:
        model = Product
        fields = [
            "name", "category", "description", "price",
            "stock", "sizes", "colors", "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Nombre del producto"}),
            "category": forms.Select(attrs={"class": SELECT_CLASSES}),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASSES, "rows": 4, "placeholder": "Descripción del producto..."}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "0.00"}),
            "stock": forms.NumberInput(attrs={"class": INPUT_CLASSES, "placeholder": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        if not product.slug:
            product.slug = slugify(product.name)
        if commit:
            product.save()
            self.save_m2m()
            image = self.cleaned_data.get("image")
            if image:
                ProductImage.objects.update_or_create(
                    product=product, is_main=True,
                    defaults={"image": image, "alt_text": product.name},
                )
        return product

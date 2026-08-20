from django import forms
from catalog.models import CarouselImage

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"
CHECKBOX_CLASSES = "w-4 h-4 rounded border-zinc-600 bg-zinc-700 theme-text-primary focus:ring-accent focus:ring-offset-0 cursor-pointer"

class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ["image", "title", "link", "order", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Título de la imagen"}),
            "link": forms.URLInput(attrs={"class": INPUT_CLASSES, "placeholder": "https://..."}),
            "order": forms.NumberInput(attrs={"class": INPUT_CLASSES}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
        }

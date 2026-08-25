from django import forms
from catalog.models import Size

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-3 py-2 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Ej: XS, S, M, L, XL, XXL, Única, 32...",
                }
            ),
        }
        labels = {
            "name": "Nombre de la Talla",
        }

from django import forms
from catalog.models import Color

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-3 py-2 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "hex_code"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Ej: Negro, Azul Marino, Verde Oliva...",
                }
            ),
            "hex_code": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES + " font-mono",
                    "placeholder": "#000000",
                    "maxlength": "7",
                }
            ),
        }
        labels = {
            "name": "Nombre del Color",
            "hex_code": "Código Hexadecimal (#RRGGBB)",
        }

    def clean_hex_code(self):
        hex_code = self.cleaned_data.get("hex_code", "").strip()
        if not hex_code.startswith("#"):
            hex_code = "#" + hex_code
        if len(hex_code) != 7:
            raise forms.ValidationError("El código hexadecimal debe tener 7 caracteres (ej: #000000).")
        try:
            int(hex_code[1:], 16)
        except ValueError:
            raise forms.ValidationError("Código hexadecimal no válido.")
        return hex_code.upper()

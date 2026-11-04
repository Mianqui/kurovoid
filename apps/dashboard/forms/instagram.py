from django import forms

from catalog.models import InstagramPost
from dashboard.models import InstagramConfig

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"
CHECKBOX_CLASSES = "w-4 h-4 rounded border-zinc-600 bg-zinc-700 theme-text-primary focus:ring-accent focus:ring-offset-0 cursor-pointer"


class InstagramConfigForm(forms.ModelForm):
    class Meta:
        model = InstagramConfig
        fields = ["activo", "titulo", "subtitulo", "usuario", "texto_boton"]
        widgets = {
            "activo": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
            "titulo": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Síguenos en Instagram"}
            ),
            "subtitulo": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Texto opcional debajo del título",
                }
            ),
            "usuario": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "kurovoid.shop"}
            ),
            "texto_boton": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Seguir en Instagram"}
            ),
        }


class InstagramPostForm(forms.ModelForm):
    class Meta:
        model = InstagramPost
        fields = ["image", "link", "alt_text", "orden", "is_active"]
        widgets = {
            "link": forms.URLInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "https://..."}
            ),
            "alt_text": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Descripción breve de la imagen",
                }
            ),
            "orden": forms.NumberInput(attrs={"class": INPUT_CLASSES, "min": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
        }
        help_texts = {
            "image": (
                "Sube una imagen cuadrada de 1080 × 1080 px (formato publicación de "
                "Instagram). Se mostrará recortada en cuadrado sin modificar el archivo original."
            ),
            "link": (
                "Si lo dejas vacío, la imagen se muestra pero no se puede clicar."
            ),
            "orden": "Menor número aparece primero.",
        }

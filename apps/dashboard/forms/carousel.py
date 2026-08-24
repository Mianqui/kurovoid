from django import forms
from catalog.models import CarouselImage
from dashboard.models import ConfiguracionTienda

INPUT_CLASSES = "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-4 py-2.5 text-sm placeholder-zinc-500 focus:outline-none focus:border-accent transition-colors"
CHECKBOX_CLASSES = "w-4 h-4 rounded border-zinc-600 bg-zinc-700 theme-text-primary focus:ring-accent focus:ring-offset-0 cursor-pointer"


class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ["image", "title", "order", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Título de la imagen (ej: Verano 2026)"}),
            "order": forms.NumberInput(attrs={"class": INPUT_CLASSES}),
            "is_active": forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
        }


class PersonalizacionForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionTienda
        fields = [
            "slider_link",
            "texto_slider_superior",
            "texto_slider_inferior",
            "texto_exclusivos_subtitulo",
            "imagen_fondo_productos",
            "texto_productos_subtitulo",
            "precio_envio",
        ]
        widgets = {
            "slider_link": forms.URLInput(attrs={"class": INPUT_CLASSES, "placeholder": "https://..."}),
            "texto_slider_superior": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Esto es Kurovoid"}),
            "texto_slider_inferior": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Tu destino de moda online"}),
            "texto_exclusivos_subtitulo": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Piezas seleccionadas con los mejores materiales y diseños que definen tu estilo."}),
            "texto_productos_subtitulo": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Explora nuestra colección completa y encuentra las prendas que se adaptan a tu personalidad."}),
            "precio_envio": forms.NumberInput(attrs={"class": INPUT_CLASSES, "step": "0.01"}),
        }

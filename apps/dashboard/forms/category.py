from django import forms

from catalog.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "image", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-3 py-2 text-sm",
                    "placeholder": "Nombre de la categoría",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-3 py-2 text-sm font-mono",
                    "placeholder": "slug-automatico",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full bg-zinc-800 border border-zinc-700 theme-text-primary rounded-lg px-3 py-2 text-sm",
                    "placeholder": "Descripción opcional",
                    "rows": 3,
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "w-full text-sm text-zinc-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-zinc-700 file:text-white hover:file:bg-zinc-600 cursor-pointer"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "rounded bg-zinc-800 border-zinc-700 theme-text-primary focus:ring-0"
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "slug": "Slug",
            "description": "Descripción",
            "image": "Imagen",
            "is_active": "Activa",
        }

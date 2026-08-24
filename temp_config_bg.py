import re

with open("apps/dashboard/models.py", "r") as f:
    content = f.read()

content = content.replace(
    'precio_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio de Envío")',
    'precio_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio de Envío")\n    imagen_fondo_productos = models.ImageField(upload_to="config/", blank=True, null=True, verbose_name="Fondo Página Productos")'
)

with open("apps/dashboard/models.py", "w") as f:
    f.write(content)

with open("apps/dashboard/views.py", "r") as f:
    views_content = f.read()

views_content = views_content.replace('fields = ["precio_envio"]', 'fields = ["precio_envio", "imagen_fondo_productos"]')
with open("apps/dashboard/views.py", "w") as f:
    f.write(views_content)

with open("templates/dashboard/configuracion.html", "r") as f:
    html_content = f.read()

html_content = html_content.replace('<form method="post">', '<form method="post" enctype="multipart/form-data">')
bg_field = """
            <div class="mb-4">
                <label class="block text-sm font-medium mb-1">Imagen de Fondo (Página Productos)</label>
                <input type="file" name="imagen_fondo_productos" class="form-input w-full bg-slate-800 border-white/10 text-white" />
                {% if form.instance.imagen_fondo_productos %}
                <p class="text-xs mt-1 text-slate-400">Actual: {{ form.instance.imagen_fondo_productos.name }}</p>
                {% endif %}
            </div>
"""
html_content = html_content.replace('<div class="mt-6 flex justify-end">', bg_field + '<div class="mt-6 flex justify-end">')

with open("templates/dashboard/configuracion.html", "w") as f:
    f.write(html_content)

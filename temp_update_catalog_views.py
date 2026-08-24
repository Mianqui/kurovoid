with open("apps/catalog/views.py", "r") as f:
    content = f.read()

import re

# Add import for ConfiguracionTienda
if "from dashboard.models import ConfiguracionTienda" not in content:
    content = content.replace("from .models import Category, Color, Product, Size, CarouselImage", "from .models import Category, Color, Product, Size, CarouselImage\nfrom dashboard.models import ConfiguracionTienda")

# Add safe load to get_context_data of ProductListView
safe_load = """
        try:
            config = ConfiguracionTienda.load()
        except Exception:
            class DummyConfig:
                imagen_fondo_productos = None
            config = DummyConfig()
        context["configuracion"] = config
        return context
"""
content = re.sub(r'return context\s*$', safe_load, content, count=1, flags=re.MULTILINE)

with open("apps/catalog/views.py", "w") as f:
    f.write(content)

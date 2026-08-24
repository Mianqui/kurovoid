import re

with open("apps/orders/views.py", "r") as f:
    content = f.read()

# Add import for ConfiguracionTienda
if "from dashboard.models import ConfiguracionTienda" not in content:
    content = content.replace("from catalog.models import Category, Color, Product, Size", "from catalog.models import Category, Color, Product, Size\nfrom dashboard.models import ConfiguracionTienda")

# In cart_detail context:
pattern_cart = re.compile(r'("selected": \{\},\n\s*\})', re.DOTALL)
content = pattern_cart.sub(r'\1\n    config = ConfiguracionTienda.load()\n    context["configuracion"] = config', content)

# In checkout view context:
pattern_checkout = re.compile(r'return render\(request, "orders/checkout\.html", \{"cart": cart\}\)')
content = pattern_checkout.sub(r'return render(request, "orders/checkout.html", {"cart": cart, "configuracion": ConfiguracionTienda.load()})', content)

with open("apps/orders/views.py", "w") as f:
    f.write(content)

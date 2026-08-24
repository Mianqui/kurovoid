with open("apps/orders/views.py", "r") as f:
    content = f.read()

import re

# Replace config = ConfiguracionTienda.load() with a safe version
safe_load = """    try:
        config = ConfiguracionTienda.load()
    except Exception:
        class DummyConfig:
            precio_envio = 0
        config = DummyConfig()"""
content = content.replace("    config = ConfiguracionTienda.load()", safe_load)

# Replace the checkout one too
safe_checkout = """
        try:
            config = ConfiguracionTienda.load()
        except Exception:
            class DummyConfig:
                precio_envio = 0
            config = DummyConfig()
        return render(request, "orders/checkout.html", {"cart": cart, "configuracion": config})
"""
content = re.sub(r'\s*return render\(request, "orders/checkout\.html", \{"cart": cart, "configuracion": ConfiguracionTienda\.load\(\)\}\)', safe_checkout, content)

with open("apps/orders/views.py", "w") as f:
    f.write(content)

import re

for filename in ["templates/orders/cart_detail.html", "templates/orders/checkout.html"]:
    with open(filename, "r") as f:
        content = f.read()

    # Add humanize load
    if "{% load static %}" in content:
        content = content.replace('{% load static %}', '{% load static humanize %}')

    # Replace Shipping logic
    content = re.sub(
        r'<th>Total de Envío :</th>\s*<td>Fijado en Dashboard \(Próximamente\)</td>',
        r'<th>Total de Envío :</th>\n                        <td>${{ configuracion.precio_envio|floatformat:0|intcomma }}</td>',
        content
    )
    
    # Calculate Total + Envío
    # We can do this in the template using the `add` filter, but since they are both decimals/floats, Django template `add` might concatenate strings if not careful, but usually it works.
    # To be safe, we can just write: ${{ cart.get_total_price|add:configuracion.precio_envio|floatformat:0|intcomma }}
    content = re.sub(
        r'<th>Total :</th>\s*<td>\$[\{a-zA-Z\.\_0-9\}]+</td>',
        r'<th>Total :</th>\n                        <td>${{ cart.get_total_price|add:configuracion.precio_envio|floatformat:0|intcomma }}</td>',
        content
    )
    
    # Format Subtotal
    content = re.sub(
        r'<th>Subtotal del Carrito :</th>\s*<td>\$\{.*?\}</td>',
        r'<th>Subtotal del Carrito :</th>\n                        <td>${{ cart.get_total_price|floatformat:0|intcomma }}</td>',
        content
    )

    with open(filename, "w") as f:
        f.write(content)

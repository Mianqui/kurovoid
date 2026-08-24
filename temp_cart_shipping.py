import re

for filename in ["templates/orders/cart_detail.html", "templates/orders/checkout.html"]:
    with open(filename, "r") as f:
        content = f.read()

    # Replace Shipping logic
    content = re.sub(
        r'<th>Total de Envío :</th>\s*<td>\$2\.00</td>',
        r'<th>Total de Envío :</th>\n                        <td>${{ configuracion.precio_envio|floatformat:0|intcomma }}</td>',
        content
    )
    
    # Format Subtotal
    content = re.sub(
        r'<th>Subtotal del Carrito :</th>\s*<td>\$\{\{\s*cart\.get_total_price\s*\}\}</td>',
        r'<th>Subtotal del Carrito :</th>\n                        <td>${{ cart.get_total_price|floatformat:0|intcomma }}</td>',
        content
    )
    
    # Total formatting
    content = re.sub(
        r'<th>Total :</th>\s*<td>\$\{\{\s*cart\.get_total_price\s*\}\}</td>',
        r'<th>Total :</th>\n                        <td>${{ cart.get_total_price|add:configuracion.precio_envio|floatformat:0|intcomma }}</td>',
        content
    )
    
    # Items formatting
    content = re.sub(r'\$\{\{\s*item\.price\s*\}\}', r'${{ item.price|floatformat:0|intcomma }}', content)
    content = re.sub(r'\$\{\{\s*item\.total_price\s*\}\}', r'${{ item.total_price|floatformat:0|intcomma }}', content)

    with open(filename, "w") as f:
        f.write(content)

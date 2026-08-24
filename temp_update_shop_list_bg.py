with open("templates/catalog/shop_product_list.html", "r") as f:
    content = f.read()

content = content.replace(
    '<section class="module bg-dark-60 shop-page-header" data-background="{% static \'images/shop/product-page-bg.jpg\' %}">',
    '<section class="module bg-dark-60 shop-page-header" data-background="{% if configuracion.imagen_fondo_productos %}{{ configuracion.imagen_fondo_productos.url }}{% else %}{% static \'images/shop/product-page-bg.jpg\' %}{% endif %}">'
)

with open("templates/catalog/shop_product_list.html", "w") as f:
    f.write(content)

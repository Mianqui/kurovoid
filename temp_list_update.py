import re

with open("templates/catalog/shop_product_list.html", "r") as f:
    content = f.read()

# Add humanize load
content = content.replace('{% load static %}', '{% load static humanize %}')

# Format prices
content = re.sub(r'\$\{\{\s*(product\.price)\s*\}\}', r'${{ \1|floatformat:0|intcomma }}', content)

# Header placeholder (1920x800)
content = re.sub(
    r'<section class="module bg-dark-60 shop-page-header" data-background="\{% static \'images/shop/product-page-bg.jpg\' %\}">',
    r'<section class="module bg-dark-60 shop-page-header" style="background-color: #333; background-image: none;">',
    content
)

# Product image placeholder
content = re.sub(
    r'\{%\s*if product\.main_image\s*%\}\{\{\s*product\.main_image\.image\.url\s*\}\}\{%\s*else\s*%\}[\s\S]*?\{%\s*endif\s*%\}',
    r'{% if product.main_image %}{{ product.main_image.image.url }}{% else %}data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22200%22%20height%3D%22250%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3C%2Fsvg%3E{% endif %}',
    content
)

with open("templates/catalog/shop_product_list.html", "w") as f:
    f.write(content)

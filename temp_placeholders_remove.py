import re

for filename in ["templates/catalog/home.html", "templates/catalog/shop_product_list.html", "templates/catalog/product_detail.html", "templates/orders/cart_detail.html", "templates/orders/checkout.html"]:
    with open(filename, "r") as f:
        content = f.read()

    # Remove SVG placeholders and restore simple static fallback (so it doesn't break layout)
    content = re.sub(
        r'data:image/svg\+xml;charset=UTF-8,%3Csvg.*?%3C%2Fsvg%3E',
        r'{% static \'images/shop/product-1.jpg\' %}',
        content
    )
    
    # Remove gray divs for empty carousels
    content = re.sub(
        r'\{%\s*empty\s*%\}[\s\S]*?<div style="background-color: #e2e8f0;.*?>[\s\S]*?</div>[\s\S]*?</div>[\s\S]*?</div>[\s\S]*?</div>',
        r'',
        content
    )
    content = re.sub(
        r'\{%\s*empty\s*%\}[\s\S]*?<li class="bg-dark-30 bg-dark shop-page-header" style="background-color: #e2e8f0;.*?</li>',
        r'',
        content
    )
    
    # Remove gray background for shop header
    content = content.replace(
        '<section class="module bg-dark-60 shop-page-header" style="background-color: #333; background-image: none;">',
        '<section class="module bg-dark-60 shop-page-header" data-background="{% static \'images/shop/product-page-bg.jpg\' %}">'
    )

    # In product detail, the main image placeholder:
    content = re.sub(
        r'<div style="background-color: #e2e8f0; width: 100%; padding-top: 100%; position: relative;"><span style="position: absolute; top: 50%; left: 50%; transform: translate\(-50%, -50%\); color: #94a3b8;">Sin imagen</span></div>',
        r'<a class="gallery" href="{% static \'images/shop/product-7.jpg\' %}"><img src="{% static \'images/shop/product-7.jpg\' %}" alt="Single Product Image"/></a>',
        content
    )

    with open(filename, "w") as f:
        f.write(content)

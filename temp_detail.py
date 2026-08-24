import re

with open("templates/product_detail.html", "r") as f:
    content = f.read()

start_idx = content.find('<section class="module">')
end_idx = content.find('<hr class="divider-d">', start_idx)

main_content = content[start_idx:end_idx]
main_content = re.sub(r'assets/([^"]+)', r"{% static '\1' %}", main_content)

# Dynamic Product Name, Price, Description
main_content = main_content.replace('Pack de Accesorios', '{{ product.name }}')
main_content = main_content.replace('£20.00', '£{{ product.price }}')

# Replace the related products section dynamically.
# Find <div class="row multi-columns-row"> and replace its contents.
pattern = re.compile(r'(<div class="row multi-columns-row">)(.*?)(</div>\s*</div>\s*</section>)', re.DOTALL)

dynamic_related = """
              {% for rp in related_products %}
              <div class="col-sm-6 col-md-3 col-lg-3">
                <div class="shop-item">
                  <div class="shop-item-image">
                    <img src="{% if rp.main_image %}{{ rp.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ rp.name }}"/>
                    <div class="shop-item-detail"><a class="btn btn-round btn-b" href="{% url 'catalog:product_detail' slug=rp.slug %}"><span class="icon-basket">Añadir al Carrito</span></a></div>
                  </div>
                  <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=rp.slug %}">{{ rp.name }}</a></h4>£{{ rp.price }}
                </div>
              </div>
              {% endfor %}
            """

main_content = pattern.sub(r'\1' + dynamic_related + r'\3', main_content)

new_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ product.name }} | Kurovoid{% endblock %}

{% block content %}
""" + main_content + """
{% endblock %}
"""

with open("templates/product_detail.html", "w") as f:
    f.write(new_content)

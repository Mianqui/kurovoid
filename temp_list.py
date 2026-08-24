import re

with open("templates/shop_product_list.html", "r") as f:
    content = f.read()

start_idx = content.find('<section class="module bg-dark-60')
end_idx = content.find('<hr class="divider-d">', start_idx)

main_content = content[start_idx:end_idx]
main_content = re.sub(r'assets/([^"]+)', r"{% static '\1' %}", main_content)

# We need to replace all product cards with a dynamic one
# Find <div class="row multi-columns-row"> and replace its contents.
pattern = re.compile(r'(<div class="row multi-columns-row">)(.*?)(<div class="row">)', re.DOTALL)

dynamic_product = """
              {% for product in products %}
              <div class="col-sm-6 col-md-3 col-lg-3">
                <div class="shop-item">
                  <div class="shop-item-image">
                    <img src="{% if product.main_image %}{{ product.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ product.name }}"/>
                    <div class="shop-item-detail"><a class="btn btn-round btn-b" href="#"><span class="icon-basket">Añadir al Carrito</span></a></div>
                  </div>
                  <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=product.slug %}">{{ product.name }}</a></h4>£{{ product.price }}
                </div>
              </div>
              {% empty %}
              <div class="col-sm-12"><p>No hay productos disponibles.</p></div>
              {% endfor %}
            </div>
            """

main_content = pattern.sub(r'\1' + dynamic_product + r'\3', main_content)

new_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}Productos | Kurovoid{% endblock %}

{% block content %}
""" + main_content + """
{% endblock %}
"""

with open("templates/shop_product_list.html", "w") as f:
    f.write(new_content)

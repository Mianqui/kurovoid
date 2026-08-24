import re

with open("templates/catalog/ejemplo.html", "r") as f:
    lines = f.readlines()

# Extract from line 60 to 297 (indices 59 to 296)
content = "".join(lines[59:297])

# Replace assets with static
content = re.sub(r'src="assets/(.*?)"', r'src="{% static \'\1\' %}"', content)
content = re.sub(r'href="assets/(.*?)"', r'href="{% static \'\1\' %}"', content)
content = re.sub(r'data-background="assets/(.*?)"', r'data-background="{% static \'\1\' %}"', content)
content = re.sub(r'url\(&quot;assets/(.*?)&quot;\)', r'url(&quot;{% static \'\1\' %}&quot;)', content)
content = re.sub(r'url\(\'assets/(.*?)\'\)', r'url(\'{% static \'\1\' %}\')', content)
content = re.sub(r'url\(assets/(.*?)\)', r'url({% static \'\1\' %})', content)

# 1. Dynamize Hero Carousel
slider_pattern = re.compile(r'(<div class="hero-slider">\s*<ul class="slides">)(.*?)(</ul>\s*</div>)', re.DOTALL)
slider_content = r"""\1
            {% for slide in carousel_images %}
            <li class="bg-dark-30 bg-dark shop-page-header" style="background-image:url('{{ slide.image.url }}');">
              <div class="titan-caption">
                <div class="caption-content">
                  <div class="font-alt mb-30 titan-title-size-1">{{ slide.title }}</div>
                  {% if slide.link %}
                  <a class="section-scroll btn btn-border-w btn-round" href="{{ slide.link }}">Saber Más</a>
                  {% endif %}
                </div>
              </div>
            </li>
            {% endfor %}
          \3"""
content = slider_pattern.sub(slider_content, content)


# 2. Dynamize "Lo último en ropa" (new_products)
new_in_pattern = re.compile(r'(<h2 class="module-title font-alt">Lo último en ropa</h2>.*?<div class="row multi-columns-row">)(.*?)(</div>\s*<div class="row mt-30">)', re.DOTALL)
new_in_content = r"""\1
              {% for product in new_products %}
              <div class="col-sm-6 col-md-3 col-lg-3">
                <div class="shop-item">
                  <div class="shop-item-image">
                    <img src="{% if product.main_image %}{{ product.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ product.name }}"/>
                    <div class="shop-item-detail"><a class="btn btn-round btn-b" href="javascript:void(0)" onclick="addToCart({{ product.id }})"><span class="icon-basket">Agregar al carrito</span></a></div>
                  </div>
                  <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=product.slug %}">{{ product.name }}</a></h4>${{ product.price|floatformat:0|intcomma }}
                </div>
              </div>
              {% endfor %}
            \3"""
content = new_in_pattern.sub(new_in_content, content)

# 3. Dynamize "Productos Destacados" (Exclusivos) (featured_products)
# First rename title
content = content.replace("Productos exclusivos", "Productos destacados")
ex_pattern = re.compile(r'(<div class="owl-carousel text-center" data-items="5" data-pagination="false" data-navigation="false">)(.*?)(</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
ex_content = r"""\1
                {% for fp in featured_products %}
                <div class="owl-item">
                  <div class="col-sm-12">
                    <div class="ex-product">
                      <a href="{% url 'catalog:product_detail' slug=fp.slug %}"><img src="{% if fp.main_image %}{{ fp.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ fp.name }}"/></a>
                      <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=fp.slug %}">{{ fp.name }}</a></h4>${{ fp.price|floatformat:0|intcomma }}
                    </div>
                  </div>
                </div>
                {% endfor %}
              \3"""
content = ex_pattern.sub(ex_content, content)

# 4. Remove "Nuestras noticias"
news_pattern = re.compile(r'<hr class="divider-w">\s*<section class="module" id="news">.*?</section>', re.DOTALL)
content = news_pattern.sub('', content)

# Combine with Django tags
final_content = "{% extends 'base.html' %}\n{% load static humanize %}\n\n{% block content %}\n" + content + "\n{% endblock %}\n"

with open("templates/catalog/home.html", "w") as f:
    f.write(final_content)

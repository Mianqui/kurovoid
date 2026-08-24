import re

with open("templates/catalog/product_detail.html", "r") as f:
    content = f.read()

content = content.replace('{% load static %}', '{% load static humanize %}')

# Format prices (product.price, rp.price, etc.)
content = re.sub(r'\$\{\{\s*([a-zA-Z0-9_]+\.price)\s*\}\}', r'${{ \1|floatformat:0|intcomma }}', content)

# Remove Related Products completely
rel_pattern = re.compile(r'<hr class="divider-w">\s*<section class="module-small">\s*<div class="container">\s*<div class="row">\s*<div class="col-sm-6 col-sm-offset-3">\s*<h2 class="module-title font-alt">Productos Relacionados.*?</section>', re.DOTALL)
content = rel_pattern.sub('', content)

# Change Productos Exclusivos to Productos Destacados
content = content.replace('Productos Exclusivos', 'Productos Destacados')

# The carousel currently iterates `featured_products` or static?
# Wait, in `product_detail.html` we had static products for exclusive. Let's make it iterate `featured_products`.
ex_pattern = re.compile(r'(<div class="owl-carousel text-center"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
dynamic_featured = r"""\1
                {% for fp in featured_products %}
                <div class="owl-item">
                  <div class="col-sm-12">
                    <div class="ex-product">
                      <a href="{% url 'catalog:product_detail' slug=fp.slug %}">
                        <img src="{% if fp.main_image %}{{ fp.main_image.image.url }}{% else %}data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22200%22%20height%3D%22250%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3C%2Fsvg%3E{% endif %}" alt="{{ fp.name }}"/>
                      </a>
                      <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=fp.slug %}">{{ fp.name }}</a></h4>${{ fp.price|floatformat:0|intcomma }}
                    </div>
                  </div>
                </div>
                {% empty %}
                <div class="owl-item">
                  <div class="col-sm-12">
                    <div class="ex-product">
                      <div style="background-color: #e2e8f0; width: 100%; padding-top: 69%; position: relative;">
                         <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #94a3b8;">Sin destacados</span>
                      </div>
                    </div>
                  </div>
                </div>
                {% endfor %}
              \3"""
content = ex_pattern.sub(dynamic_featured, content)

# Main image placeholder
content = re.sub(
    r'<a class="gallery" href="\{% static \'images/shop/product-7\.jpg\' %\}">\s*<img src="\{% static \'images/shop/product-7\.jpg\' %\}" alt="Single Product Image"/>\s*</a>',
    r'<div style="background-color: #e2e8f0; width: 100%; padding-top: 100%; position: relative;"><span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #94a3b8;">Sin imagen</span></div>',
    content
)

with open("templates/catalog/product_detail.html", "w") as f:
    f.write(content)

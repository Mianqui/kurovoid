import re

with open("templates/catalog/product_detail.html", "r") as f:
    content = f.read()

# Replace the static images gallery block
# Search for <div class="col-sm-6 mb-sm-40">...</ul>\n              </div>
pattern = re.compile(r'(<div class="col-sm-6 mb-sm-40">)(.*?)(</ul>\s*</div>)', re.DOTALL)
dynamic_images = """
                {% if product.main_image %}
                <a class="gallery" href="{{ product.main_image.image.url }}">
                  <img src="{{ product.main_image.image.url }}" alt="{{ product.name }}"/>
                </a>
                {% else %}
                <a class="gallery" href="{% static 'images/shop/product-7.jpg' %}">
                  <img src="{% static 'images/shop/product-7.jpg' %}" alt="Single Product Image"/>
                </a>
                {% endif %}
                <ul class="product-gallery">
                  {% for img in product.images.all %}
                  {% if not img.is_main %}
                  <li><a class="gallery" href="{{ img.image.url }}"></a><img src="{{ img.image.url }}" alt="Gallery Image"/></li>
                  {% endif %}
                  {% endfor %}
"""
content = pattern.sub(r'\1' + dynamic_images + r'\3', content)

# Replace description
desc_pattern = re.compile(r'(<div class="description">\s*<p>).*?(</p>\s*</div>)', re.DOTALL)
content = desc_pattern.sub(r'\1{{ product.description }}\2', content)

# Replace categories
cat_pattern = re.compile(r'(<div class="product_meta">Categorías:).*?(</div>)', re.DOTALL)
dynamic_cats = """
<a href="{% url 'catalog:category_list' slug=product.category.slug %}"> {{ product.category.name }} </a>
"""
content = cat_pattern.sub(r'\1' + dynamic_cats + r'\2', content)

# Replace tab description
tab_desc_pattern = re.compile(r'(<div class="tab-pane active" id="description">)(.*?)(</div>)', re.DOTALL)
content = tab_desc_pattern.sub(r'\1<p>{{ product.description }}</p>\3', content)

with open("templates/catalog/product_detail.html", "w") as f:
    f.write(content)

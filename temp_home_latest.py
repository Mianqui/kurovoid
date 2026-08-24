import re

with open("templates/catalog/home.html", "r") as f:
    content = f.read()

# Replace latest products
pattern = re.compile(r'(<div class="row multi-columns-row">)(.*?)(<div class="row mt-30">)', re.DOTALL)
dynamic_latest = r"""\1
              {% for product in new_products %}
              <div class="col-sm-6 col-md-3 col-lg-3">
                <div class="shop-item">
                  <div class="shop-item-image">
                    <img src="{% if product.main_image %}{{ product.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ product.name }}"/>
                    <div class="shop-item-detail">
                      <a class="btn btn-round btn-b" href="#" onclick="event.preventDefault(); addToCart({{ product.id }});">
                        <span class="icon-basket">Añadir al Carrito</span>
                      </a>
                    </div>
                  </div>
                  <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=product.slug %}">{{ product.name }}</a></h4>${{ product.price }}
                </div>
              </div>
              {% endfor %}
            </div>
            \3"""
content = pattern.sub(dynamic_latest, content, count=1)

# The second occurrence of <div class="row multi-columns-row"> is for News, we skip it.
# Now for "Productos Exclusivos"
# <div class="owl-carousel text-center" data-items="5" data-pagination="false" data-navigation="false">
pattern_carousel = re.compile(r'(<div class="owl-carousel text-center"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
dynamic_exclusive = r"""\1
                {% for product in new_products %}
                <div class="owl-item">
                  <div class="col-sm-12">
                    <div class="ex-product">
                      <a href="{% url 'catalog:product_detail' slug=product.slug %}">
                        <img src="{% if product.main_image %}{{ product.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ product.name }}"/>
                      </a>
                      <h4 class="shop-item-title font-alt"><a href="{% url 'catalog:product_detail' slug=product.slug %}">{{ product.name }}</a></h4>${{ product.price }}
                    </div>
                  </div>
                </div>
                {% endfor %}
              \3"""
content = pattern_carousel.sub(dynamic_exclusive, content, count=1)

with open("templates/catalog/home.html", "w") as f:
    f.write(content)

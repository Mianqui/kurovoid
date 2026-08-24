import re

with open("templates/catalog/home.html", "r") as f:
    content = f.read()

# Replace carousel
pattern = re.compile(r'(<div class="hero-slider">\s*<ul class="slides">)(.*?)(</ul>\s*</div>)', re.DOTALL)
dynamic_carousel = r"""\1
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
            {% empty %}
            <li class="bg-dark-30 bg-dark shop-page-header" style="background-image:url('{% static 'images/shop/slider1.png' %}');">
              <div class="titan-caption">
                <div class="caption-content">
                  <div class="font-alt mb-30 titan-title-size-1">Bienvenido a Kurovoid</div>
                </div>
              </div>
            </li>
            {% endfor %}
            \3"""

content = pattern.sub(dynamic_carousel, content)

# Replace £ with $
content = content.replace('£', '$')

with open("templates/catalog/home.html", "w") as f:
    f.write(content)

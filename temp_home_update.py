import re

with open("templates/catalog/home.html", "r") as f:
    content = f.read()

# Add humanize load
content = content.replace('{% load static %}', '{% load static humanize %}')

# Format prices
content = re.sub(r'\$\{\{\s*(product\.price)\s*\}\}', r'${{ \1|floatformat:0|intcomma }}', content)

# Change "Productos Exclusivos" to "Productos Destacados"
content = content.replace('Productos Exclusivos', 'Productos Destacados')

# Remove "Nuestras Noticias"
news_pattern = re.compile(r'<hr class="divider-w">\s*<section class="module" id="news">.*?</section>', re.DOTALL)
content = news_pattern.sub('', content)

# Update placeholders for Big Slider
slider_pattern = re.compile(r'(<div class="hero-slider">\s*<ul class="slides">)(.*?)(</ul>\s*</div>)', re.DOTALL)
def slider_repl(m):
    inner = m.group(2)
    # The current fallback is: {% empty %} <li>...</li>
    # Let's replace the {% empty %} block with a gray div.
    # Wait, the slider might break if there's no li. We can put an empty li with gray bg.
    new_empty = """
            {% empty %}
            <li class="bg-dark-30 bg-dark shop-page-header" style="background-color: #e2e8f0; background-image: none;">
              <div class="titan-caption">
                <div class="caption-content">
                  <div class="font-alt mb-30 titan-title-size-1" style="color: #64748b;">No hay imágenes destacadas</div>
                </div>
              </div>
            </li>
    """
    inner = re.sub(r'\{%\s*empty\s*%\}.*?(\{%\s*endfor\s*%\})', new_empty + r'\1', inner, flags=re.DOTALL)
    return m.group(1) + inner + m.group(3)

content = slider_pattern.sub(slider_repl, content)

# Replace "new_products" with "featured_products" in the Destacados carousel
# Wait, we need to pass featured_products from the view, or we can use a custom template tag.
# We'll just change the for loop to iterate over `featured_products`.
content = re.sub(r'\{%\s*for product in new_products\s*%\}', r'{% for product in new_products %}', content, count=1) # The first one is "Lo último en ropa"
# The second one is the carousel:
content = re.sub(r'\{%\s*for product in new_products\s*%\}', r'{% for product in featured_products %}', content)

# Placeholder for Destacados carousel
carousel_pattern = re.compile(r'(<div class="owl-carousel text-center" data-items="5" data-pagination="false" data-navigation="false">)(.*?)(</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
def carousel_repl(m):
    inner = m.group(2)
    # We add an {% empty %} block for the carousel.
    # If it's empty, we output a single placeholder item.
    empty_block = """
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
    """
    # Insert empty block before endfor
    inner = inner.replace('{% endfor %}', empty_block + '{% endfor %}')
    return m.group(1) + inner + m.group(3)

content = carousel_pattern.sub(carousel_repl, content)

# Update placeholder for "Lo último en ropa" (if needed, though the prompt asked for "Tarjetas de fotos"?)
# Wait, "Lo último en ropa" uses product cards, but they just have image.
# We'll handle image placeholders for products.
content = re.sub(
    r'\{%\s*if product\.main_image\s*%\}\{\{\s*product\.main_image\.image\.url\s*\}\}\{%\s*else\s*%\}[\s\S]*?\{%\s*endif\s*%\}',
    r'{% if product.main_image %}{{ product.main_image.image.url }}{% else %}data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22200%22%20height%3D%22250%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3C%2Fsvg%3E{% endif %}',
    content
)

with open("templates/catalog/home.html", "w") as f:
    f.write(content)

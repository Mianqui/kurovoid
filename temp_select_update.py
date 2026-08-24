with open("templates/catalog/shop_product_list.html", "r") as f:
    content = f.read()

import re

# Gender select update
gender_pattern = re.compile(r'(<select class="form-control"[^>]*>)\s*<option selected="selected">Mujer</option>\s*<option>Hombre</option>\s*(</select>)')
content = gender_pattern.sub(r'\1\n                  <option selected="selected">Hombre</option>\n                  <option>Mujer</option>\n                \2', content)

# Category select update
# Replace the whole <select> with a dynamic one
cat_pattern = re.compile(r'(<select class="form-control"[^>]*>)\s*<option selected="selected">Todo</option>.*?(</select>)', re.DOTALL)
cat_replacement = r"""<select class="form-control" name="category">
                  <option value="" {% if not request.GET.category %}selected="selected"{% endif %}>Todo</option>
                  {% for c in categories %}
                  <option value="{{ c.slug }}" {% if request.GET.category == c.slug %}selected="selected"{% endif %}>{{ c.name }}</option>
                  {% endfor %}
                </select>"""
content = cat_pattern.sub(cat_replacement, content)

with open("templates/catalog/shop_product_list.html", "w") as f:
    f.write(content)

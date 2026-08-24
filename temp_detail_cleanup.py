import re

with open("templates/catalog/product_detail.html", "r") as f:
    content = f.read()

# Remove stars and reviews link below title
content = re.sub(r'<div class="row mb-20">\s*<div class="col-sm-12"><span><i class="fa fa-star.*?</div>\s*</div>', '', content, flags=re.DOTALL)

# Remove Reviews tab
content = re.sub(r'<li><a href="#reviews" data-toggle="tab"><span class="icon-tools-2"></span>Valoraciones.*?</a></li>', '', content)

# Remove Reviews tab-pane completely
content = re.sub(r'<div class="tab-pane" id="reviews">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', '</div></div></div></div>', content, flags=re.DOTALL)

# Make Data Sheet dynamic
pattern = re.compile(r'(<div class="tab-pane" id="data-sheet">\s*<table class="table table-striped ds-table table-responsive">\s*<tbody>).*?(</tbody>\s*</table>\s*</div>)', re.DOTALL)
dynamic_sheet = r"""\1
                        <tr>
                          <th>Título</th>
                          <th>Información</th>
                        </tr>
                        <tr>
                          <td>Categoría</td>
                          <td>{{ product.category.name|default:"Sin categoría" }}</td>
                        </tr>
                        <tr>
                          <td>Tallas disponibles</td>
                          <td>
                            {% for size in product.sizes.all %}
                              {{ size.name }}{% if not forloop.last %}, {% endif %}
                            {% empty %}
                              Única
                            {% endfor %}
                          </td>
                        </tr>
                        <tr>
                          <td>Colores</td>
                          <td>
                            {% for color in product.colors.all %}
                              {{ color.name }}{% if not forloop.last %}, {% endif %}
                            {% empty %}
                              Único
                            {% endfor %}
                          </td>
                        </tr>
                      \2"""
content = pattern.sub(dynamic_sheet, content)

with open("templates/catalog/product_detail.html", "w") as f:
    f.write(content)

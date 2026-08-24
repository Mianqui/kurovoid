import re

with open("templates/orders/cart_detail.html", "r") as f:
    content = f.read()

# Replace the table rows with dynamic Django loop
pattern = re.compile(r'(<tbody>\s*<tr>\s*<th class="hidden-xs">Artículo</th>.*?</tr>)(.*?)(</tbody>)', re.DOTALL)
dynamic_cart = r"""\1
                    {% for item in cart %}
                    <tr>
                      <td class="hidden-xs"><a href="{% url 'catalog:product_detail' slug=item.product.slug %}"><img src="{% if item.product.main_image %}{{ item.product.main_image.image.url }}{% else %}{% static 'images/shop/product-1.jpg' %}{% endif %}" alt="{{ item.product.name }}"/></a></td>
                      <td>
                        <h5 class="product-title font-alt">{{ item.product.name }}</h5>
                      </td>
                      <td class="hidden-xs">
                        <h5 class="product-title font-alt">£{{ item.price }}</h5>
                      </td>
                      <td>
                        <input class="form-control" type="number" name="quantity" value="{{ item.quantity }}" max="50" min="1"/>
                      </td>
                      <td>
                        <h5 class="product-title font-alt">£{{ item.total_price }}</h5>
                      </td>
                      <td class="pr-remove"><a href="#" title="Eliminar" onclick="event.preventDefault(); fetch('{% url 'orders:cart_remove' product_id=item.product.id %}', {method: 'POST', headers: {'X-CSRFToken': '{{ csrf_token }}'}}).then(()=>location.reload())"><i class="fa fa-times"></i></a></td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6">Tu carrito está vacío.</td></tr>
                    {% endfor %}
                    \3"""
content = pattern.sub(dynamic_cart, content)

# Replace Cart Totals
content = re.sub(r'£40\.00', r'£{{ cart.get_total_price }}', content)
content = re.sub(r'£42\.00', r'£{{ cart.get_total_price }}', content)

# Update form/checkout link
content = content.replace('type="submit">Proceder al Pago', 'type="button" onclick="location.href=\'{% url \'orders:checkout\' %}\'">Proceder al Pago')

with open("templates/orders/cart_detail.html", "w") as f:
    f.write(content)

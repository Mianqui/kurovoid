with open("templates/orders/cart_detail.html", "r") as f:
    content = f.read()

# Replace the input to trigger update on change
content = content.replace(
    '<input class="form-control" type="number" name="quantity" value="{{ item.quantity }}" max="50" min="1"/>',
    '<input class="form-control cart-qty-input" data-id="{{ item.product.id }}" type="number" name="quantity" value="{{ item.quantity }}" max="50" min="1"/>'
)

# Replace the table rows wrapper to easily update them?
# No, we can just reload the page on change, or actually update via JS. The user said "al cambiar la cantidad se deberia ajusta el precio total automaticamente".
# Fetch API on change -> updates the backend, then updates the page or reloads it.
# Easiest way to "update automatically" is just `location.reload()` on success!
import re
pattern = re.compile(r'({% endblock %})', re.DOTALL)
js = """
<script>
document.querySelectorAll('.cart-qty-input').forEach(input => {
    input.addEventListener('change', function() {
        let productId = this.getAttribute('data-id');
        let quantity = this.value;
        fetch("{% url 'orders:cart_update' product_id=0 %}".replace('0', productId), {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'quantity=' + quantity
        }).then(res => res.json()).then(data => {
            if(data.success) {
                location.reload(); // Recargar para mostrar los nuevos totales
            }
        });
    });
});
</script>
"""
content = pattern.sub(js + r'\n\1', content)

# Fix Shipping and Total
content = re.sub(r'<tr>\s*<th>Total de Envío :</th>\s*<td>\$2\.00</td>\s*</tr>', 
    r'<tr>\n                        <th>Total de Envío :</th>\n                        <td>Fijado en Dashboard (Próximamente)</td>\n                      </tr>', content)

with open("templates/orders/cart_detail.html", "w") as f:
    f.write(content)

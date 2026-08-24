with open("templates/catalog/product_detail.html", "r") as f:
    content = f.read()

# Replace the form with a button that calls fetch
# Currently it is:
# <form method="post" action="{% url 'orders:cart_add' product_id=product.id %}">
#   {% csrf_token %}
#   <input type="hidden" name="quantity" value="1" id="cart-quantity-hidden" />
#   <button class="btn btn-lg btn-block btn-round btn-b" type="submit">Añadir al Carrito</button>
# </form>
# <script>...</script>

import re
pattern = re.compile(r'<form method="post" action=".*?">.*?</script>', re.DOTALL)
dynamic_add = """
                    <button class="btn btn-lg btn-block btn-round btn-b" type="button" onclick="addToCartDetail()">Añadir al Carrito</button>
                    <script>
                      function addToCartDetail() {
                          let qty = document.querySelector('input[type="number"]').value;
                          fetch("{% url 'orders:cart_add' product_id=product.id %}", {
                              method: 'POST',
                              headers: {
                                  'X-CSRFToken': '{{ csrf_token }}',
                                  'Content-Type': 'application/x-www-form-urlencoded'
                              },
                              body: 'quantity=' + qty
                          })
                          .then(response => response.json())
                          .then(data => {
                              if(data.success) {
                                  alert('Producto añadido al carrito');
                              }
                          });
                      }
                    </script>
"""

content = pattern.sub(dynamic_add.strip(), content)

# Also fix £ to $
content = content.replace('£', '$')

with open("templates/catalog/product_detail.html", "w") as f:
    f.write(content)

import re

with open("templates/catalog/shop_product_list.html", "r") as f:
    content = f.read()

pattern = re.compile(r'(<div class="pagination font-alt">)(.*?)(</div>)', re.DOTALL)
dynamic_pagination = r"""\1
                  {% if page_obj.has_previous %}
                  <a href="?page={{ page_obj.previous_page_number }}"><i class="fa fa-angle-left"></i></a>
                  {% endif %}
                  
                  {% for num in page_obj.paginator.page_range %}
                    {% if page_obj.number == num %}
                      <a class="active" href="#">{{ num }}</a>
                    {% else %}
                      <a href="?page={{ num }}">{{ num }}</a>
                    {% endif %}
                  {% endfor %}
                  
                  {% if page_obj.has_next %}
                  <a href="?page={{ page_obj.next_page_number }}"><i class="fa fa-angle-right"></i></a>
                  {% endif %}
                \3"""
content = pattern.sub(dynamic_pagination, content)

# Also fix the pounds to dollars in the product card
content = content.replace('£', '$')

with open("templates/catalog/shop_product_list.html", "w") as f:
    f.write(content)

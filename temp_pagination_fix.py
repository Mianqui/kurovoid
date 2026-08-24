with open("templates/catalog/shop_product_list.html", "r") as f:
    content = f.read()

import re

# We will replace "?page=X" with "?page=X{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}"
query_params = "{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}"

content = re.sub(
    r'\?page=\{\{\s*page_obj\.previous_page_number\s*\}\}',
    r'?page={{ page_obj.previous_page_number }}' + query_params,
    content
)
content = re.sub(
    r'\?page=\{\{\s*num\s*\}\}',
    r'?page={{ num }}' + query_params,
    content
)
content = re.sub(
    r'\?page=\{\{\s*page_obj\.next_page_number\s*\}\}',
    r'?page={{ page_obj.next_page_number }}' + query_params,
    content
)

with open("templates/catalog/shop_product_list.html", "w") as f:
    f.write(content)

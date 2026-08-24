import re

with open("templates/shop_checkout.html", "r") as f:
    content = f.read()

start_idx = content.find('<section class="module">')
end_idx = content.find('<hr class="divider-d">', start_idx)

main_content = content[start_idx:end_idx]
main_content = re.sub(r'assets/([^"]+)', r"{% static '\1' %}", main_content)

new_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}Checkout | Kurovoid{% endblock %}

{% block content %}
""" + main_content + """
{% endblock %}
"""

with open("templates/shop_checkout.html", "w") as f:
    f.write(new_content)

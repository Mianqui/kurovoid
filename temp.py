import re

with open("templates/index.html", "r") as f:
    content = f.read()

# Extract the content between the nav and footer
# It's basically everything from <section class="home-section... to right before <hr class="divider-d">\n<footer...
start_idx = content.find('<section class="home-section')
end_idx = content.find('<hr class="divider-d">', start_idx)

main_content = content[start_idx:end_idx]

# Replace assets/ with {% static '...' %}
main_content = re.sub(r'assets/([^"]+)', r"{% static '\1' %}", main_content)

new_content = """{% extends 'base.html' %}
{% load static %}

{% block content %}
""" + main_content + """
{% endblock %}
"""

with open("templates/index.html", "w") as f:
    f.write(new_content)

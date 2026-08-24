with open("static/js/main.js", "r") as f:
    content = f.read()

import re

# Update owlCarousel options
pattern = re.compile(r'(\$\(this\)\.owlCarousel\(\s*\{)(.*?)(\}\);)', re.DOTALL)
def repl(m):
    inner = m.group(2)
    # We add smartSpeed and adjust others
    if 'smartSpeed' not in inner:
        # Just replace the whole block or insert it
        pass
    return m.group(1) + """
                navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
                nav: navigation,
                dots: pagination,
                loop: true,
                dotsSpeed: 400,
                items: items,
                navSpeed: 300,
                autoplay: true,
                autoplayTimeout: 4000,
                autoplayHoverPause: true,
                smartSpeed: 500,
                fluidSpeed: 500
""" + m.group(3)

content = pattern.sub(repl, content)

with open("static/js/main.js", "w") as f:
    f.write(content)

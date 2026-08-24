with open("apps/dashboard/views.py", "r") as f:
    content = f.read()

# Add ConfiguracionTienda view
config_view = """
from .models import ConfiguracionTienda
from django.urls import reverse_lazy

@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class ConfiguracionView(UpdateView):
    model = ConfiguracionTienda
    fields = ["precio_envio"]
    template_name = "dashboard/configuracion.html"
    success_url = reverse_lazy("dashboard:configuracion")

    def get_object(self):
        return ConfiguracionTienda.load()

    def form_valid(self, form):
        messages.success(self.request, "Configuración guardada exitosamente.")
        return super().form_valid(form)
"""
if "class ConfiguracionView" not in content:
    content += "\n" + config_view

with open("apps/dashboard/views.py", "w") as f:
    f.write(content)

with open("apps/dashboard/urls.py", "r") as f:
    urls_content = f.read()

if "views.ConfiguracionView.as_view()" not in urls_content:
    urls_content = urls_content.replace(
        ']',
        '    path("configuracion/", views.ConfiguracionView.as_view(), name="configuracion"),\n]'
    )
with open("apps/dashboard/urls.py", "w") as f:
    f.write(urls_content)


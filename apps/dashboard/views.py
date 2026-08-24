from datetime import date, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Prefetch, Q, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.models import Category as CategoryModel, Product, ProductImage, CarouselImage
from orders.models import Pedido, PedidoItem

from .forms.category import CategoryForm

from .forms.category import CategoryForm
from .forms.product import ProductForm
from .forms.carousel import CarouselImageForm

from django.conf import settings
decorators = [login_required, staff_member_required(login_url=settings.LOGIN_URL)]


@method_decorator(decorators, name="dispatch")
class DashboardHomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = Product.objects.count()
        context["total_categories"] = CategoryModel.objects.count()
        context["out_of_stock"] = Product.objects.filter(stock=0).count()
        context["low_stock"] = Product.objects.filter(stock__gt=0, stock__lte=3).count()
        context["latest_products"] = Product.objects.order_by("-created_at")[:5]
        context["out_of_stock_products"] = (
            Product.objects.select_related("category")
            .prefetch_related(
                Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="_main_images")
            )
            .filter(stock=0)
            .order_by("name")[:5]
        )
        context["low_stock_products"] = (
            Product.objects.select_related("category")
            .prefetch_related(
                Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="_main_images")
            )
            .filter(stock__gt=0, stock__lte=3)
            .order_by("stock")[:5]
        )
        return context


@method_decorator(decorators, name="dispatch")
class ProductListAdminView(ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.select_related("category").prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="_main_images")
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(category__name__icontains=q)
            )
        return qs


@method_decorator(decorators, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    success_url = reverse_lazy("dashboard:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    context_object_name = "product"
    success_url = reverse_lazy("dashboard:product_list")
    pk_url_kwarg = "pk"

    def get_initial(self):
        initial = super().get_initial()
        product = self.get_object()
        main_img = product.images.filter(is_main=True).first()
        if main_img:
            initial["image"] = main_img.image
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"] = True
        context["main_image"] = self.get_object().images.filter(is_main=True).first()
        context["product_images"] = (
            self.get_object().images.all().order_by("orden", "id")
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "dashboard/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("dashboard:product_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class VentasView(TemplateView):
    template_name = "dashboard/ventas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hoy = date.today()
        hace_30_dias = hoy - timedelta(days=30)
        inicio_mes_actual = hoy.replace(day=1)
        mes_anterior = inicio_mes_actual - timedelta(days=1)
        inicio_mes_anterior = mes_anterior.replace(day=1)

        # --- Datos para gráfica de línea (ingresos últimos 30 días) ---
        ingresos_diarios = (
            Pedido.objects.filter(
                creado_en__gte=hace_30_dias,
                estado__in=["confirmado", "enviado", "entregado"],
            )
            .annotate(fecha=TruncDate("creado_en"))
            .values("fecha")
            .annotate(total=Sum("total"))
            .order_by("fecha")
        )

        fechas = []
        montos = []
        fecha_actual = hace_30_dias
        ingresos_dict = {r["fecha"]: float(r["total"]) for r in ingresos_diarios if r["fecha"]}
        while fecha_actual <= hoy:
            fechas.append(fecha_actual.strftime("%d/%m"))
            montos.append(ingresos_dict.get(fecha_actual, 0))
            fecha_actual += timedelta(days=1)

        context["line_fechas"] = fechas
        context["line_montos"] = montos

        # --- Datos para gráfica de barras (pedidos por estado) ---
        estados = Pedido.ESTADO_CHOICES
        pedidos_por_estado = (
            Pedido.objects.values("estado")
            .annotate(total=Count("id"))
            .order_by("estado")
        )
        estado_counts = {r["estado"]: r["total"] for r in pedidos_por_estado}
        context["bar_estados"] = [e[0] for e in estados]
        context["bar_etiquetas"] = [e[1] for e in estados]
        context["bar_totales"] = [estado_counts.get(e[0], 0) for e in estados]

        # --- Cards de resumen ---
        ventas_mes_actual = Pedido.objects.filter(
            creado_en__gte=inicio_mes_actual,
            estado__in=["confirmado", "enviado", "entregado"],
        ).aggregate(total=Sum("total"))["total"] or 0

        ventas_mes_anterior = Pedido.objects.filter(
            creado_en__gte=inicio_mes_anterior,
            creado_en__lt=inicio_mes_actual,
            estado__in=["confirmado", "enviado", "entregado"],
        ).aggregate(total=Sum("total"))["total"] or 0

        if ventas_mes_anterior > 0:
            cambio_pct = ((ventas_mes_actual - ventas_mes_anterior) / ventas_mes_anterior) * 100
        else:
            cambio_pct = 100 if ventas_mes_actual > 0 else 0

        pedidos_completados = Pedido.objects.filter(
            estado="entregado", creado_en__gte=inicio_mes_actual
        ).count()

        ticket_promedio = Pedido.objects.filter(
            creado_en__gte=hace_30_dias,
            estado__in=["confirmado", "enviado", "entregado"],
        ).aggregate(promedio=Sum("total") / Count("id"))

        promedio_valor = 0
        tp = Pedido.objects.filter(
            creado_en__gte=hace_30_dias,
            estado__in=["confirmado", "enviado", "entregado"],
        ).aggregate(total=Sum("total"), count=Count("id"))
        if tp["count"] and tp["count"] > 0:
            promedio_valor = float(tp["total"]) / tp["count"]

        context["ventas_mes_actual"] = ventas_mes_actual
        context["cambio_pct"] = round(cambio_pct, 1)
        context["cambio_positivo"] = cambio_pct >= 0
        context["pedidos_completados"] = pedidos_completados
        context["ticket_promedio"] = round(promedio_valor, 2)

        return context


@method_decorator(decorators, name="dispatch")
class OrderListView(ListView):
    model = Pedido
    template_name = "dashboard/pedido_list.html"
    context_object_name = "pedidos"
    paginate_by = 20

    def get_queryset(self):
        qs = Pedido.objects.select_related("usuario").prefetch_related("items__producto")

        estado = self.request.GET.get("estado")
        fecha = self.request.GET.get("fecha")
        q = self.request.GET.get("q")

        if estado:
            qs = qs.filter(estado=estado)

        hoy = date.today()
        if fecha == "hoy":
            qs = qs.filter(creado_en__date=hoy)
        elif fecha == "semana":
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            qs = qs.filter(creado_en__date__gte=inicio_semana)
        elif fecha == "mes":
            inicio_mes = hoy.replace(day=1)
            qs = qs.filter(creado_en__date__gte=inicio_mes)

        if q:
            qs = qs.filter(
                Q(nombre_cliente__icontains=q)
                | Q(telefono__icontains=q)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ESTADOS"] = Pedido.ESTADO_CHOICES
        context["selected_estado"] = self.request.GET.get("estado", "")
        context["selected_fecha"] = self.request.GET.get("fecha", "")
        context["selected_q"] = self.request.GET.get("q", "")
        return context


@method_decorator(decorators, name="dispatch")
class OrderDetailView(DetailView):
    model = Pedido
    template_name = "dashboard/pedido_detail.html"
    context_object_name = "pedido"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Pedido.objects.select_related("usuario").prefetch_related(
            "items__producto__images", "items__producto__category"
        )

    def post(self, request, *args, **kwargs):
        pedido = self.get_object()
        nuevo_estado = request.POST.get("estado")
        numero_guia = request.POST.get("numero_guia", "")

        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            if nuevo_estado == "enviado" and numero_guia:
                pedido.numero_guia = numero_guia
            pedido.save(update_fields=["estado", "numero_guia"])
            messages.success(request, f"Pedido actualizado a {pedido.get_estado_display()}.")

        return redirect("dashboard:pedido_detail", pk=pedido.id)


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


@method_decorator([login_required], name="dispatch")
class UserListView(SuperUserRequiredMixin, ListView):
    model = User
    template_name = "dashboard/usuario_list.html"
    context_object_name = "usuarios"
    paginate_by = 20

    def get_queryset(self):
        qs = User.objects.filter(is_staff=False).order_by("-date_joined")

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(username__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
            )

        orden = self.request.GET.get("orden", "reciente")
        if orden == "pedidos":
            qs = qs.annotate(num_pedidos=Count("pedido")).order_by("-num_pedidos")
        elif orden == "gastado":
            qs = qs.annotate(
                total_gastado=Sum("pedido__total", filter=Q(pedido__estado__in=["confirmado", "enviado", "entregado"]))
            ).order_by("-total_gastado")
        else:
            qs = qs.order_by("-date_joined")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_q"] = self.request.GET.get("q", "")
        context["selected_orden"] = self.request.GET.get("orden", "reciente")

        for u in context["usuarios"]:
            u.pedidos_count = Pedido.objects.filter(usuario=u).count()
            u.total_gastado = (
                Pedido.objects.filter(usuario=u, estado__in=["confirmado", "enviado", "entregado"])
                .aggregate(t=Sum("total"))["t"]
                or 0
            )

        return context


@method_decorator([login_required], name="dispatch")
class UserDetailView(SuperUserRequiredMixin, DetailView):
    model = User
    template_name = "dashboard/usuario_detail.html"
    context_object_name = "usuario"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.get_object()

        pedidos = Pedido.objects.filter(usuario=user_obj).order_by("-creado_en")
        context["pedidos"] = pedidos

        total_gastado = pedidos.filter(
            estado__in=["confirmado", "enviado", "entregado"]
        ).aggregate(t=Sum("total"))["t"] or 0
        context["total_gastado"] = total_gastado

        primer_pedido = pedidos.last()
        ultimo_pedido = pedidos.first()
        context["primer_pedido"] = primer_pedido.creado_en if primer_pedido else None
        context["ultimo_pedido"] = ultimo_pedido.creado_en if ultimo_pedido else None

        context["tiene_pedidos_activos"] = pedidos.exclude(estado="entregado").exclude(estado="cancelado").exists()

        return context

    def post(self, request, *args, **kwargs):
        user_obj = self.get_object()
        tiene_activos = (
            Pedido.objects.filter(usuario=user_obj)
            .exclude(estado="entregado")
            .exclude(estado="cancelado")
            .exists()
        )
        if tiene_activos:
            messages.error(
                request,
                f"No se puede eliminar a {user_obj.get_full_name() or user_obj.username}. Tiene pedidos activos.",
            )
        else:
            user_obj.delete()
            messages.success(request, "Usuario eliminado correctamente.")
            return redirect("dashboard:usuario_list")

        return redirect("dashboard:usuario_detail", pk=user_obj.id)


@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class CategoryListView(ListView):
    model = CategoryModel
    template_name = "dashboard/categoria_list.html"
    context_object_name = "categorias"
    ordering = ["orden", "name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for cat in context["categorias"]:
            cat.productos_activos = cat.products.filter(is_active=True).count()
        return context


@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class CategoryCreateView(CreateView):
    model = CategoryModel
    form_class = CategoryForm
    template_name = "dashboard/categoria_form.html"
    success_url = reverse_lazy("dashboard:categoria_list")

    def form_valid(self, form):
        messages.success(self.request, "Categoría creada exitosamente.")
        return super().form_valid(form)


@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class CategoryUpdateView(UpdateView):
    model = CategoryModel
    form_class = CategoryForm
    template_name = "dashboard/categoria_form.html"
    context_object_name = "categoria"
    success_url = reverse_lazy("dashboard:categoria_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"] = True
        return context


@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class CategoryDeleteView(DeleteView):
    model = CategoryModel
    template_name = "dashboard/categoria_confirm_delete.html"
    context_object_name = "categoria"
    success_url = reverse_lazy("dashboard:categoria_list")
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = self.get_object()
        context["has_products"] = cat.products.exists()
        return context

    def form_valid(self, form):
        cat = self.get_object()
        if cat.products.exists():
            messages.error(self.request, "No se puede eliminar una categoría con productos asociados.")
            return redirect("dashboard:categoria_list")
        messages.success(self.request, "Categoría eliminada.")
        return super().form_valid(form)


@require_POST
@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def categoria_reordenar(request):
    import json
    data = json.loads(request.body)
    ids = data.get("ids", [])
    for idx, cat_id in enumerate(ids):
        CategoryModel.objects.filter(id=cat_id).update(orden=idx)
    return JsonResponse({"success": True})


@require_POST
@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def categoria_toggle_active(request, pk):
    cat = get_object_or_404(CategoryModel, id=pk)
    cat.is_active = not cat.is_active
    cat.save(update_fields=["is_active"])
    return JsonResponse({"success": True, "is_active": cat.is_active})


@method_decorator([login_required, staff_member_required(login_url=settings.LOGIN_URL)], name="dispatch")
class AlertasView(ListView):
    model = Product
    template_name = "dashboard/alertas.html"
    context_object_name = "productos"

    def get_queryset(self):
        return (
            Product.objects.select_related("category")
            .prefetch_related(
                Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="_main_images")
            )
            .filter(stock__lte=3)
            .order_by("stock")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_alertas"] = self.get_queryset().count()
        return context


@require_POST
@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_reponer_stock(request, pk):
    import json
    data = json.loads(request.body)
    nueva_cantidad = data.get("cantidad")
    if nueva_cantidad is None or not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
        return JsonResponse({"success": False, "error": "Cantidad inválida"}, status=400)
    producto = get_object_or_404(Product, id=pk)
    producto.stock = nueva_cantidad
    producto.save(update_fields=["stock"])
    return JsonResponse({
        "success": True,
        "stock": producto.stock,
        "nivel": producto.nivel_stock,
    })


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_subir_imagen(request, pk):
    producto = get_object_or_404(Product, id=pk)
    if producto.images.count() >= 10:
        return JsonResponse({"success": False, "error": "Límite de 10 imágenes alcanzado."}, status=400)

    archivos = request.FILES.getlist("files")
    subidas = []
    for archivo in archivos:
        if producto.images.count() >= 10:
            break
        img = ProductImage.objects.create(
            product=producto,
            image=archivo,
        )
        subidas.append({
            "id": img.id,
            "url": img.image.url,
            "alt_text": img.alt_text,
            "is_main": img.is_main,
            "orden": img.orden,
        })
    return JsonResponse({"success": True, "images": subidas})


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_eliminar_imagen(request, img_id):
    img = get_object_or_404(ProductImage, id=img_id)
    img.delete()
    return JsonResponse({"success": True})


@require_POST
@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_reordenar_imagenes(request, pk):
    import json
    data = json.loads(request.body)
    ids = data.get("ids", [])
    for idx, img_id in enumerate(ids):
        ProductImage.objects.filter(id=img_id).update(orden=idx)
    return JsonResponse({"success": True})


@require_POST
@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_imagen_principal(request, img_id):
    img = get_object_or_404(ProductImage, id=img_id)
    ProductImage.objects.filter(product=img.product, is_main=True).update(is_main=False)
    img.is_main = True
    img.save(update_fields=["is_main"])
    return JsonResponse({"success": True, "is_main": True})


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def producto_actualizar_alt_text(request, img_id):
    import json
    data = json.loads(request.body)
    alt_text = data.get("alt_text", "")
    img = get_object_or_404(ProductImage, id=img_id)
    img.alt_text = alt_text
    img.save(update_fields=["alt_text"])
    return JsonResponse({"success": True})


import csv

from django.http import HttpResponse


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def ExportProductosCSV(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    writer.writerow(["ID", "Nombre", "Categoría", "Precio", "Stock", "Activo", "Creado"])
    for p in Product.objects.select_related("category").iterator():
        writer.writerow([
            p.id,
            p.name,
            p.category.name,
            p.price,
            p.stock,
            "Sí" if p.is_active else "No",
            p.created_at.strftime("%Y-%m-%d") if p.created_at else "",
        ])
    return response


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def ExportPedidosCSV(request):
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")
    qs = Pedido.objects.select_related("usuario").order_by("-creado_en")
    if desde:
        qs = qs.filter(creado_en__date__gte=desde)
    if hasta:
        qs = qs.filter(creado_en__date__lte=hasta)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pedidos.csv"'
    writer = csv.writer(response)
    writer.writerow(["Número", "Cliente", "Email", "Estado", "Total", "Fecha"])
    for pedido in qs.iterator():
        writer.writerow([
            pedido.numero_pedido,
            pedido.nombre_cliente or (pedido.usuario.get_full_name() or pedido.usuario.username) if pedido.usuario else "",
            pedido.usuario.email if pedido.usuario else "",
            pedido.get_estado_display(),
            pedido.total,
            pedido.creado_en.strftime("%Y-%m-%d"),
        ])
    return response


from .models import ConfiguracionTienda
from .forms.carousel import PersonalizacionForm

@method_decorator(decorators, name="dispatch")
class PersonalizacionView(UpdateView):
    model = ConfiguracionTienda
    form_class = PersonalizacionForm
    template_name = "dashboard/personalizacion.html"
    success_url = reverse_lazy("dashboard:personalizacion")

    def get_object(self):
        return ConfiguracionTienda.load()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_images"] = CarouselImage.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Personalización guardada exitosamente.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class CarouselCreateView(CreateView):
    model = CarouselImage
    form_class = CarouselImageForm
    template_name = "dashboard/carousel_form.html"
    success_url = reverse_lazy("dashboard:personalizacion")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["editing"] = False
        return ctx

@method_decorator(decorators, name="dispatch")
class CarouselUpdateView(UpdateView):
    model = CarouselImage
    form_class = CarouselImageForm
    template_name = "dashboard/carousel_form.html"
    success_url = reverse_lazy("dashboard:personalizacion")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["editing"] = True
        return ctx

@method_decorator(decorators, name="dispatch")
class CarouselDeleteView(DeleteView):
    model = CarouselImage
    template_name = "dashboard/carousel_confirm_delete.html"
    success_url = reverse_lazy("dashboard:personalizacion")


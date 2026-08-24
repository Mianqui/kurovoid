from catalog.models import Category, Color, Product, Size
from dashboard.models import ConfiguracionTienda
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST
from decimal import Decimal

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    try:
        config = ConfiguracionTienda.load()
    except Exception:

        class DummyConfig:
            precio_envio = 0

        config = DummyConfig()
    context = {
        "cart": cart,
        "categories": Category.objects.all(),
        "sizes": Size.objects.all(),
        "colors": Color.objects.all(),
        "price_range": Product.objects.filter(is_active=True).aggregate(
            min_price=Min("price"), max_price=Max("price")
        ),
        "selected": {},
        "configuracion": config,
        "cart_total_with_shipping": cart.get_total_price() + Decimal(str(config.precio_envio)),
    }
    return render(request, "orders/cart_detail.html", context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")
    cart.add(product, quantity, size, color)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))
    if quantity > 0:
        cart.update(product_id, quantity)
    else:
        cart.remove(product_id)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )


class CheckoutView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile.email_verificado:
            if not profile.token_es_valido():
                from users.email_utils import enviar_email_verificacion

                enviar_email_verificacion(request.user, request)
                messages.warning(
                    request,
                    "Te enviamos un enlace de verificación a tu correo. "
                    "Debes verificarlo antes de realizar un pedido.",
                )
            else:
                messages.warning(
                    request,
                    "Debes verificar tu correo antes de realizar un pedido. "
                    "Revisa tu bandeja de entrada.",
                )
            return redirect("orders:cart_detail")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        cart = Cart(request)
        if not cart:
            messages.info(request, "Tu carrito está vacío.")
            return redirect("orders:cart_detail")
        try:
            config = ConfiguracionTienda.load()
        except Exception:

            class DummyConfig:
                precio_envio = 0

            config = DummyConfig()
            
        cart_total_with_shipping = cart.get_total_price() + Decimal(str(config.precio_envio))
        return render(
            request, "orders/checkout.html", {"cart": cart, "configuracion": config, "cart_total_with_shipping": cart_total_with_shipping}
        )

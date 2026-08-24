from asgiref.sync import sync_to_async
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def enviar_email_verificacion(usuario, request):
    profile = usuario.profile
    token = profile.generar_token_verificacion()
    dominio = request.get_host()
    protocolo = "https" if request.is_secure() else "http"
    link = f"{protocolo}://{dominio}/cuenta/verificar-email/{token}/"

    contexto = {
        "usuario": usuario,
        "link": link,
        "expira": "24 horas",
    }

    asunto = "Verifica tu correo — Kurovoid"
    cuerpo_txt = render_to_string("emails/verificacion.txt", contexto)
    cuerpo_html = render_to_string("emails/verificacion.html", contexto)

    email = EmailMultiAlternatives(
        subject=asunto,
        body=cuerpo_txt,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[usuario.email],
    )
    email.attach_alternative(cuerpo_html, "text/html")
    email.send(fail_silently=False)


enviar_email_verificacion_async = sync_to_async(enviar_email_verificacion, thread_sensitive=True)

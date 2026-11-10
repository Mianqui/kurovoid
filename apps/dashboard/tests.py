import json
import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from catalog.models import InstagramPost

from dashboard.forms.instagram import InstagramConfigForm, InstagramPostForm
from dashboard.models import InstagramConfig

TEST_MEDIA_ROOT = tempfile.mkdtemp()
TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}


def make_image(name="instagram.png"):
    """Crea una imagen PNG de 1 × 1 px para las pruebas."""
    buffer = BytesIO()
    Image.new("RGB", (1, 1), color=(0, 0, 0)).save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, STORAGES=TEST_STORAGES)
class InstagramDashboardTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff",
            password="clave-segura",
            is_staff=True,
        )

    def test_anonymous_user_is_redirected(self):
        response = self.client.get(reverse("dashboard:instagram"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_non_staff_user_is_redirected(self):
        user = User.objects.create_user(username="cliente", password="clave-segura")
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard:instagram"))

        self.assertEqual(response.status_code, 302)

    def test_config_forms_have_no_api_fields(self):
        self.assertEqual(
            set(InstagramConfigForm().fields),
            {"activo", "titulo", "subtitulo", "usuario", "texto_boton"},
        )
        self.assertEqual(
            set(InstagramPostForm().fields),
            {"image", "link", "alt_text", "orden", "is_active"},
        )

    def test_staff_can_see_posts_and_config(self):
        self.client.force_login(self.staff)
        InstagramPost.objects.create(
            image=make_image(),
            alt_text="Imagen visible en el panel",
            is_active=True,
        )

        response = self.client.get(reverse("dashboard:instagram"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carrusel de Instagram")
        self.assertContains(response, "Imagen visible en el panel")

    def test_staff_can_create_post_with_square_image(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("dashboard:instagram_post_create"),
            {
                "image": make_image(),
                "link": "https://example.com/publicacion",
                "alt_text": "Nueva imagen",
                "orden": 3,
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        post = InstagramPost.objects.get()
        self.assertEqual(post.link, "https://example.com/publicacion")
        self.assertEqual(post.alt_text, "Nueva imagen")
        self.assertEqual(post.orden, 3)
        self.assertTrue(post.is_active)

    def test_staff_can_create_post_without_link(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("dashboard:instagram_post_create"),
            {
                "image": make_image(),
                "link": "",
                "alt_text": "Sin enlace",
                "orden": 0,
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        post = InstagramPost.objects.get()
        self.assertEqual(post.link, "")
        self.assertTrue(post.is_active)

    def test_staff_can_update_post(self):
        self.client.force_login(self.staff)
        post = InstagramPost.objects.create(
            image=make_image(),
            alt_text="Antes",
            orden=1,
            is_active=True,
        )

        response = self.client.post(
            reverse("dashboard:instagram_post_update", args=[post.pk]),
            {
                "link": "https://example.com/actualizada",
                "alt_text": "Después",
                "orden": 9,
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        post.refresh_from_db()
        self.assertEqual(post.link, "https://example.com/actualizada")
        self.assertEqual(post.alt_text, "Después")
        self.assertEqual(post.orden, 9)

    def test_staff_can_delete_post(self):
        self.client.force_login(self.staff)
        post = InstagramPost.objects.create(
            image=make_image(),
            alt_text="Se va a eliminar",
            is_active=True,
        )

        response = self.client.post(
            reverse("dashboard:instagram_post_delete", args=[post.pk])
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        self.assertFalse(InstagramPost.objects.filter(pk=post.pk).exists())

    def test_staff_can_delete_post_via_ajax(self):
        self.client.force_login(self.staff)
        post = InstagramPost.objects.create(
            image=make_image(),
            alt_text="Se elimina sin recargar",
            is_active=True,
        )

        response = self.client.post(
            reverse("dashboard:instagram_post_ajax_delete", args=[post.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertFalse(InstagramPost.objects.filter(pk=post.pk).exists())

    def test_staff_can_reorder_posts(self):
        self.client.force_login(self.staff)
        primero = InstagramPost.objects.create(
            image=make_image("a.png"), alt_text="A", orden=0
        )
        segundo = InstagramPost.objects.create(
            image=make_image("b.png"), alt_text="B", orden=1
        )
        tercero = InstagramPost.objects.create(
            image=make_image("c.png"), alt_text="C", orden=2
        )

        response = self.client.post(
            reverse("dashboard:instagram_reordenar"),
            data=json.dumps({"ids": [tercero.pk, primero.pk, segundo.pk]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        primero.refresh_from_db()
        segundo.refresh_from_db()
        tercero.refresh_from_db()
        self.assertEqual(tercero.orden, 0)
        self.assertEqual(primero.orden, 1)
        self.assertEqual(segundo.orden, 2)

    def test_reorder_rejects_invalid_json(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("dashboard:instagram_reordenar"),
            data="no-es-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"success": False, "error": "Datos inválidos."},
        )

    def test_staff_can_update_instagram_config(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("dashboard:instagram"),
            {
                "activo": "on",
                "titulo": "Nuestro Instagram",
                "subtitulo": "Síguenos para ver las novedades",
                "usuario": "kurovoid.store",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        config = InstagramConfig.load()
        self.assertTrue(config.activo)
        self.assertEqual(config.titulo, "Nuestro Instagram")
        self.assertEqual(config.subtitulo, "Síguenos para ver las novedades")
        self.assertEqual(config.usuario, "kurovoid.store")

    def test_staff_can_deactivate_instagram_section(self):
        self.client.force_login(self.staff)
        config = InstagramConfig.load()
        config.activo = True
        config.save()

        response = self.client.post(
            reverse("dashboard:instagram"),
            {
                "titulo": config.titulo,
                "subtitulo": config.subtitulo,
                "usuario": config.usuario,
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        config.refresh_from_db()
        self.assertFalse(config.activo)

    def test_staff_can_edit_texto_boton(self):
        self.client.force_login(self.staff)
        config = InstagramConfig.load()

        response = self.client.post(
            reverse("dashboard:instagram"),
            {
                "activo": "on",
                "titulo": config.titulo,
                "subtitulo": config.subtitulo,
                "usuario": config.usuario,
                "texto_boton": "Ver mi Instagram",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        config.refresh_from_db()
        self.assertEqual(config.texto_boton, "Ver mi Instagram")

    def test_titulo_puede_estar_vacio(self):
        self.client.force_login(self.staff)
        config = InstagramConfig.load()

        response = self.client.post(
            reverse("dashboard:instagram"),
            {
                "activo": "on",
                "titulo": "",
                "subtitulo": config.subtitulo,
                "usuario": config.usuario,
                "texto_boton": config.texto_boton,
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        config.refresh_from_db()
        self.assertEqual(config.titulo, "")

    def test_staff_can_upload_real_image(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("dashboard:instagram_post_create"),
            {
                "image": make_image("subida_real.png"),
                "link": "",
                "alt_text": "Imagen subida desde el panel",
                "orden": 0,
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:instagram"))
        post = InstagramPost.objects.get()
        self.assertTrue(post.image.name.endswith(".png"))
        self.assertTrue(post.image.storage.exists(post.image.name))
        self.assertEqual(post.alt_text, "Imagen subida desde el panel")

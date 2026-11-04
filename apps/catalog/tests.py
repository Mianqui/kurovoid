import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from catalog.models import InstagramPost

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
class HomeInstagramTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.config = InstagramConfig.load()

    def test_section_hidden_when_config_inactive(self):
        self.config.activo = False
        self.config.save()
        InstagramPost.objects.create(image=make_image(), is_active=True)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "instagram-section")

    def test_section_hidden_without_active_posts(self):
        InstagramPost.objects.create(image=make_image(), is_active=False)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "instagram-section")

    def test_section_shows_only_active_posts_in_order(self):
        second = InstagramPost.objects.create(
            image=make_image("segunda.png"),
            alt_text="Segunda imagen",
            orden=2,
            is_active=True,
        )
        first = InstagramPost.objects.create(
            image=make_image("primera.png"),
            alt_text="Primera imagen",
            orden=1,
            is_active=True,
        )
        InstagramPost.objects.create(
            image=make_image("inactiva.png"),
            alt_text="Imagen inactiva",
            orden=0,
            is_active=False,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "instagram-section")
        self.assertEqual(
            list(response.context["instagram_posts"]),
            [first, second],
        )
        self.assertContains(response, "Primera imagen")
        self.assertContains(response, "Segunda imagen")
        self.assertNotContains(response, "Imagen inactiva")

    def test_section_limits_posts_to_twelve(self):
        for index in range(13):
            InstagramPost.objects.create(
                image=make_image(f"imagen-{index}.png"),
                orden=index,
                is_active=True,
            )

        response = self.client.get(reverse("home"))

        self.assertEqual(len(response.context["instagram_posts"]), 12)

    def test_post_with_link_is_clickable(self):
        post = InstagramPost.objects.create(
            image=make_image(),
            link="https://example.com/publicacion",
            alt_text="Con enlace",
            is_active=True,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, f'href="{post.link}"')
        self.assertContains(response, "instagram-card--link", count=1)
        self.assertContains(response, 'target="_blank"')

    def test_post_without_link_is_not_clickable(self):
        InstagramPost.objects.create(
            image=make_image(),
            alt_text="Sin enlace",
            is_active=True,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Sin enlace")
        self.assertNotContains(response, "instagram-card--link")

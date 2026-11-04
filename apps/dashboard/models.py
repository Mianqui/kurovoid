from django.db import models


class ConfiguracionTienda(models.Model):
    imagen_fondo_productos = models.ImageField(upload_to="config/", blank=True, null=True, verbose_name="Fondo Página Productos")
    
    # Link general para el botón "Saber Más" del slider
    slider_link = models.URLField(blank=True, verbose_name="Link del Slider (Saber Más)", help_text="URL del botón 'Saber Más' en el slider de inicio")
    
    # Textos editables del slider de inicio
    texto_slider_superior = models.CharField(max_length=200, blank=True, verbose_name="Texto superior del slider", help_text="Texto pequeño arriba del título (ej: 'Esto es Kurovoid')")
    texto_slider_inferior = models.CharField(max_length=200, blank=True, verbose_name="Texto inferior del slider", help_text="Texto debajo del título (ej: 'Tu destino de moda online')")
    
    # Subtítulo de la sección "Productos Exclusivos" en home
    texto_exclusivos_subtitulo = models.CharField(max_length=300, blank=True, verbose_name="Subtítulo Productos Exclusivos", help_text="Texto bajo el título 'Productos Exclusivos' en la página de inicio")
    
    # Subtítulo de la página de productos
    texto_productos_subtitulo = models.CharField(max_length=300, blank=True, verbose_name="Subtítulo Página Productos", help_text="Texto bajo el título en la página de productos")
    
    class Meta:
        verbose_name = "Configuración de Tienda"
        verbose_name_plural = "Configuraciones de Tienda"
        
    def __str__(self):
        return "Configuración Global"
        
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class InstagramConfig(models.Model):
    activo = models.BooleanField(default=True)
    titulo = models.CharField(max_length=150, blank=True, default="")
    subtitulo = models.CharField(max_length=300, blank=True)
    usuario = models.CharField(max_length=100, default="kurovoid.shop")
    texto_boton = models.CharField(max_length=100, default="Seguir en Instagram", blank=True)

    class Meta:
        verbose_name = "Configuración del carrusel de Instagram"
        verbose_name_plural = "Configuración del carrusel de Instagram"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

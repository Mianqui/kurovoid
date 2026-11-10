# Kurovoid

Tienda online construida con Django y Tailwind CSS.

## Requisitos

- Python 3.14+
- Node.js (para Tailwind CSS)
- PostgreSQL (en Docker) o SQLite (local)

## Instalación

```bash
# Clonar e instalar dependencias
pip install -r requirements.txt
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Migraciones y servidor
python manage.py migrate
python manage.py runserver
```

## Docker

### Desarrollo local

```bash
cp .env.example .env
docker compose -f compose.dev.yml up --build
```

El servicio `web` aplica las migraciones automáticamente y queda disponible en `http://localhost:8000`. Para cargar datos de demostración:

```bash
docker compose -f compose.dev.yml exec web python manage.py seed_data
```

Para crear un administrador:

```bash
docker compose -f compose.dev.yml exec web python manage.py createsuperuser
```

Para detener el entorno:

```bash
docker compose -f compose.dev.yml down
```

### Producción

El archivo `compose.yml` usa la imagen publicada en GHCR y está pensado para el despliegue automático al hacer push a `main`. No se debe compilar localmente:

```bash
docker compose up -d
```

## Tailwind CSS

```bash
npm run build:css
```

## Carrusel de Instagram

El inicio incluye un carrusel manual de imágenes verticales (4:5) después de la sección "Productos Destacados". No utiliza la API de Instagram, tokens ni sincronización automática: las imágenes y sus enlaces se administran desde el panel.

### Administración

1. Entra a `/dashboard/instagram/` con un usuario staff.
2. Activa o desactiva la sección y edita el título, el subtítulo, el usuario de Instagram y el texto del botón. Todos los textos son opcionales.
3. Sube imágenes de 1080 × 1350 px. Se recomienda ese tamaño; cualquier imagen se recorta en formato 4:5 sin deformarse.
4. Cada imagen puede tener un enlace fijo que se abre en una pestaña nueva. Si el enlace se deja vacío, la imagen se muestra pero no es clicable.
5. Usa las flechas de cada tarjeta o arrástrala desde su número para cambiar el orden; el nuevo orden se guarda sin recargar. Los botones **Editar** y **Eliminar** permiten modificar o borrar cada tarjeta.
6. La sección incluye una vista previa con el mismo diseño del inicio.

La sección solo se muestra en el inicio cuando está activa y existe al menos una imagen activa. En móvil se ven 2 imágenes, en tablet 3 y en escritorio 4.

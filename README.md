# Kurovoid

Tienda online construida con Django, Bootstrap y CSS propio. No utiliza Tailwind ni requiere Node.js.

## Requisitos

- Python 3.14+
- PostgreSQL 16 (recomendado con Docker) o SQLite (local)
- Docker y Docker Compose (opcional, para desarrollo o producción)

## Instalación local

```bash
pip install -r requirements.txt

# Crear el archivo de entorno
cp .env.example .env
# En Windows PowerShell:
# Copy-Item .env.example .env

# Editar .env con tus valores locales
python manage.py migrate
python manage.py runserver
```

Si prefieres SQLite, ajusta en `.env`:

```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## Docker

### Desarrollo local

Usa siempre `compose.dev.yml` para desarrollo. El compose de producción (`compose.yml`) está reservado para el servidor.

```bash
cp .env.example .env
docker compose -f compose.dev.yml up --build
```

El servicio `web` aplica las migraciones automáticamente y queda disponible en `http://localhost:8000`.

Para cargar datos de demostración:

```bash
docker compose -f compose.dev.yml exec web python manage.py seed_data
```

El usuario demo `cliente` se crea sin contraseña de acceso. Para asignarle una, define `SEED_CLIENT_PASSWORD` en el archivo `.env` antes de ejecutar el comando, o cámbiala después con:

```bash
docker compose -f compose.dev.yml exec web python manage.py changepassword cliente
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

El archivo `compose.yml` usa la imagen publicada en GHCR y está pensado para el despliegue automático. No se debe compilar localmente:

```bash
docker compose up -d
```

## Pruebas

```bash
# Con Docker de desarrollo
docker compose -f compose.dev.yml exec web python manage.py check
docker compose -f compose.dev.yml exec web python manage.py test apps.catalog apps.dashboard apps.orders

# Verificar que no falten migraciones
docker compose -f compose.dev.yml exec web python manage.py makemigrations --check --dry-run
```

## Despliegue

- Solo la rama `main` (o una ejecución manual autorizada del workflow) dispara el despliegue (`.github/workflows/deploy.yml`).
- El flujo recomendado es trabajar en una rama, abrir un Pull Request y mergear a `main` cuando las pruebas pasen.
- El workflow construye la imagen, la publica en `ghcr.io/mianqui/kurovoid:latest`, copia `compose.yml` al servidor y ejecuta las migraciones.
- Los secretos de producción se configuran únicamente en **GitHub → Settings → Secrets and variables → Actions**. Nunca deben escribirse en el repositorio, en el README ni en archivos versionados.
- No modifiques `compose.yml` para desarrollo local; usa `compose.dev.yml`.

## Variables de entorno

Copia `.env.example` como `.env` y completa los valores. `.env` está ignorado por Git y no debe subirse.

| Variable | Descripción |
| --- | --- |
| `SECRET_KEY` | Clave secreta de Django. Debe ser única y segura en producción. |
| `DEBUG` | `True` en desarrollo, `False` en producción. |
| `ALLOWED_HOSTS` | Dominios permitidos, separados por coma. |
| `DB_ENGINE` | `django.db.backends.postgresql` o `django.db.backends.sqlite3`. |
| `DB_NAME` | Nombre de la base de datos. |
| `DB_USER` | Usuario de la base de datos. |
| `DB_PASSWORD` | Contraseña de la base de datos. |
| `DB_HOST` | Host de la base de datos (`db` en Docker). |
| `DB_PORT` | Puerto de PostgreSQL (`5432` por defecto). |
| `EMAIL_HOST` | Servidor SMTP. |
| `EMAIL_PORT` | Puerto SMTP. |
| `EMAIL_HOST_USER` | Usuario SMTP. |
| `EMAIL_HOST_PASSWORD` | Contraseña o clave de aplicación SMTP. |
| `EMAIL_USE_TLS` | `True` para conexiones TLS. |
| `DEFAULT_FROM_EMAIL` | Remitente de los correos. |
| `SECURE_SSL_REDIRECT` | Controla la redirección de HTTP a HTTPS según el proxy de producción. |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables para CSRF, separados por coma. |
| `SESSION_COOKIE_SECURE` | Cookies de sesión solo por HTTPS en producción. |
| `CSRF_COOKIE_SECURE` | Cookies CSRF solo por HTTPS en producción. |

No documentes ni compartas valores reales de estas variables.

## Seguridad y confidencialidad

- `.env` está en `.gitignore`. No lo versiones ni pegues su contenido en issues, chats o capturas.
- En producción usa `DEBUG=False`, una `SECRET_KEY` robusta y HTTPS con HSTS.
- Las rutas `/admin`, `/dashboard` y `/auth` están restringidas a redes privadas mediante `config/middleware.py`. Para acceso remoto usa la VPN o el túnel autorizado; no desactives esta protección.
- El panel requiere usuario staff. Aplica el principio de menor privilegio y no compartas cuentas.
- Los secretos de CI/CD viven en GitHub Actions Secrets. No los incluyas en el código ni en la documentación.
- Revisa las dependencias y mantén actualizado `requirements.txt`.
- No subas respaldos de base de datos, archivos `.env`, claves privadas ni credenciales al repositorio.

## Estructura del proyecto

```text
apps/
  catalog/      Productos, categorías, colores, tallas y carrusel de Instagram
  dashboard/    Panel de administración y configuración de la tienda
  orders/       Carrito y pedidos
  users/        Autenticación y usuarios
config/         Configuración Django, URLs, WSGI/ASGI y middleware
templates/      Plantillas del sitio y del panel
static/         CSS, JavaScript, imágenes y librerías locales
media/          Archivos subidos (ignorado por Git)
compose.dev.yml Compose para desarrollo
compose.yml     Compose para producción
Dockerfile      Imagen de producción
```

## Estilos y assets

- Los estilos están en `static/css/`: `base.css`, `dashboard.css`, `storefront.css`, `style.css` y `colors/`.
- No hay paso de compilación de CSS. Edita los archivos directamente.
- Bootstrap, Owl Carousel y las demás librerías están incluidas localmente en `static/lib/`.
- Al modificar `style.css` o `main.js`, actualiza el parámetro `?v=` en `templates/base.html` para invalidar la caché y recarga con `Ctrl + F5`.
- En Docker, `collectstatic` se ejecuta durante la construcción de la imagen y WhiteNoise sirve los archivos estáticos en producción.

## Carrusel de Instagram

El inicio incluye un carrusel manual de imágenes verticales (4:5) después de la sección "Productos Destacados" y antes del footer. No utiliza la API de Instagram, tokens ni sincronización automática: las imágenes y sus enlaces se administran desde el panel.

### Administración

1. Entra a `/dashboard/instagram/` con un usuario staff.
2. Activa o desactiva la sección y edita el título, el subtítulo, el usuario de Instagram y el texto del botón. Todos los textos son opcionales.
3. El campo `usuario` solo se usa para construir el enlace del botón CTA. El handle `@usuario` no se muestra en el home.
4. Sube imágenes de 1080 × 1350 px. Se recomienda ese tamaño; cualquier imagen se recorta en formato 4:5 sin deformarse.
5. Cada imagen puede tener un enlace fijo que se abre en una pestaña nueva. Si el enlace se deja vacío, la imagen se muestra pero no es clicable.
6. Usa las flechas de cada tarjeta o arrástrala desde su número para cambiar el orden; el nuevo orden se guarda sin recargar. Los botones **Editar** y **Eliminar** permiten modificar o borrar cada tarjeta.
7. El panel no incluye vista previa; los cambios se ven directamente en el inicio.

La sección solo se muestra en el inicio cuando está activa y existe al menos una imagen activa. En móvil se ven 2 imágenes, en tablet 3 y en escritorio 4. Las esquinas son rectas y las imágenes se guardan en `media/instagram/`.

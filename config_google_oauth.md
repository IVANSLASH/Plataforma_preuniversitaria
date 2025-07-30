# Configuración de Google OAuth - Plataforma Preuniversitaria

## Requisitos Previos

1. **Cuenta de Google Developer**: Necesitas una cuenta de Google y acceso a Google Cloud Console
2. **Proyecto en Google Cloud**: Crear un proyecto en Google Cloud Console
3. **Credenciales OAuth**: Configurar las credenciales OAuth 2.0

## Pasos para Configurar Google OAuth

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ (si no está habilitada)

### 2. Configurar Credenciales OAuth 2.0

1. En Google Cloud Console, ve a **APIs & Services** > **Credentials**
2. Haz clic en **Create Credentials** > **OAuth 2.0 Client IDs**
3. Selecciona **Web application**
4. Configura las URLs de redirección autorizadas:
   - `http://localhost:5000/auth/google/callback` (desarrollo)
   - `https://tu-dominio.com/auth/google/callback` (producción)

### 3. Obtener Credenciales

Después de crear las credenciales, obtendrás:
- **Client ID**: ID del cliente OAuth
- **Client Secret**: Secreto del cliente OAuth

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Google OAuth
GOOGLE_CLIENT_ID=tu_client_id_aqui
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# Otras configuraciones
SECRET_KEY=tu_clave_secreta_aqui
FLASK_ENV=development
```

### 5. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 6. Actualizar Base de Datos

Si ya tienes una base de datos existente, necesitas agregar las nuevas columnas:

```sql
-- Agregar columnas para Google OAuth
ALTER TABLE usuarios ADD COLUMN google_id VARCHAR(100) UNIQUE;
ALTER TABLE usuarios ADD COLUMN google_picture VARCHAR(500);
ALTER TABLE usuarios ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local';
```

O simplemente elimina el archivo `plataforma.db` y deja que se recree automáticamente.

## Configuración para Producción

### 1. URLs de Redirección

En Google Cloud Console, agrega las URLs de redirección de producción:
- `https://tu-dominio.com/auth/google/callback`
- `https://www.tu-dominio.com/auth/google/callback`

### 2. Configuración de Seguridad

```env
# Producción
FLASK_ENV=production
SECRET_KEY=clave_secreta_muy_segura_y_larga
GOOGLE_CLIENT_ID=tu_client_id_produccion
GOOGLE_CLIENT_SECRET=tu_client_secret_produccion
```

### 3. Configuración de HTTPS

Asegúrate de que tu aplicación use HTTPS en producción, ya que Google OAuth requiere conexiones seguras.

## Verificación de la Configuración

### 1. Probar Login con Google

1. Inicia la aplicación: `python app.py`
2. Ve a `/auth/login`
3. Haz clic en "Continuar con Google"
4. Deberías ser redirigido a Google para autorización
5. Después de autorizar, deberías volver a la aplicación

### 2. Verificar Base de Datos

```python
from app import app
from models import db, Usuario

with app.app_context():
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        print(f"Usuario: {usuario.username}, Provider: {usuario.auth_provider}")
```

## Solución de Problemas

### Error: "redirect_uri_mismatch"

- Verifica que las URLs de redirección en Google Cloud Console coincidan exactamente con las configuradas en tu aplicación
- Asegúrate de incluir tanto `http://localhost:5000` como `https://tu-dominio.com`

### Error: "invalid_client"

- Verifica que el Client ID y Client Secret sean correctos
- Asegúrate de que las credenciales estén configuradas como variables de entorno

### Error: "access_denied"

- El usuario canceló la autorización en Google
- Verifica que la aplicación esté configurada correctamente en Google Cloud Console

### Usuario no se crea en la base de datos

- Verifica los logs de la aplicación para errores
- Asegúrate de que la base de datos tenga las columnas necesarias
- Verifica que las credenciales de Google sean válidas

## Características Implementadas

### ✅ Funcionalidades Completadas

1. **Login con Google**: Los usuarios pueden iniciar sesión usando su cuenta de Google
2. **Registro con Google**: Los usuarios pueden registrarse usando su cuenta de Google
3. **Vinculación de Cuentas**: Si un usuario ya existe con el mismo email, se vincula la cuenta de Google
4. **Información de Perfil**: Se muestra si el usuario se registró con Google o localmente
5. **Protección de Rutas**: Los usuarios de Google no pueden cambiar contraseña desde la aplicación
6. **Interfaz de Usuario**: Botones de Google en las páginas de login y registro

### 🔧 Configuración Técnica

- **OAuth 2.0**: Implementación completa del flujo de autorización
- **Verificación de Tokens**: Validación segura de tokens de Google
- **Manejo de Sesiones**: Integración con Flask-Login
- **Base de Datos**: Campos adicionales para información de Google
- **Seguridad**: Protección CSRF y validación de estado

## Próximos Pasos (Opcionales)

1. **Más Proveedores**: Agregar soporte para Facebook, GitHub, etc.
2. **Perfil de Google**: Mostrar foto de perfil de Google en la interfaz
3. **Sincronización**: Sincronizar información del perfil con Google
4. **Notificaciones**: Enviar notificaciones por email de Google
5. **Analytics**: Seguimiento de usuarios por proveedor de autenticación 
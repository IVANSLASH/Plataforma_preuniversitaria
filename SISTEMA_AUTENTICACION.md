# Sistema de Autenticación - Plataforma Preuniversitaria

## 📋 Descripción General

El sistema de autenticación implementado proporciona un control completo de acceso a la plataforma preuniversitaria, incluyendo registro de usuarios, inicio de sesión, gestión de perfiles y administración de usuarios.

## 🚀 Características Principales

### ✅ Funcionalidades Implementadas

- **Registro de usuarios** con validación completa
- **Inicio de sesión** con opción "Recordarme"
- **Gestión de perfiles** de usuario
- **Cambio de contraseñas** seguro
- **Sistema de roles** (usuario normal y administrador)
- **Administración de usuarios** (solo para admins)
- **Sesiones seguras** con tracking
- **Validación de formularios** en tiempo real
- **Interfaz moderna** y responsiva

### 🔐 Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF
- Sesiones seguras
- Validación de entrada
- Control de acceso por roles

## 📁 Estructura de Archivos

```
├── models.py                 # Modelos de base de datos
├── auth.py                   # Rutas de autenticación
├── config.py                 # Configuración de la aplicación
├── templates/auth/           # Templates de autenticación
│   ├── login.html           # Página de inicio de sesión
│   ├── register.html        # Página de registro
│   ├── profile.html         # Perfil de usuario
│   ├── edit_profile.html    # Editar perfil
│   ├── change_password.html # Cambiar contraseña
│   └── admin_users.html     # Administración de usuarios
└── plataforma.db            # Base de datos SQLite
```

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno (Opcional)

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_muy_segura
DATABASE_URL=sqlite:///plataforma.db
LOG_LEVEL=INFO
```

### 3. Ejecutar la Aplicación

```bash
python app.py
```

La base de datos se creará automáticamente con un usuario administrador por defecto:
- **Usuario:** admin
- **Contraseña:** admin123

## 📊 Modelo de Datos

### Tabla: usuarios

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único del usuario |
| username | String(80) | Nombre de usuario único |
| email | String(120) | Email único |
| password_hash | String(255) | Hash de la contraseña |
| nombre_completo | String(100) | Nombre completo |
| fecha_registro | DateTime | Fecha de registro |
| ultimo_acceso | DateTime | Último acceso |
| es_activo | Boolean | Estado de la cuenta |
| es_admin | Boolean | Es administrador |
| institucion | String(100) | Institución educativa |
| nivel_educativo | String(50) | Nivel educativo |
| materias_favoritas | Text | Materias favoritas (JSON) |
| preferencias | Text | Preferencias (JSON) |

### Tabla: sesiones_usuario

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único de la sesión |
| usuario_id | Integer | ID del usuario |
| fecha_inicio | DateTime | Inicio de sesión |
| fecha_fin | DateTime | Fin de sesión |
| ip_address | String(45) | Dirección IP |
| user_agent | Text | User Agent del navegador |

## 🔗 Rutas Disponibles

### Rutas Públicas
- `GET /auth/login` - Página de inicio de sesión
- `POST /auth/login` - Procesar inicio de sesión
- `GET /auth/register` - Página de registro
- `POST /auth/register` - Procesar registro

### Rutas Protegidas (Requieren autenticación)
- `GET /auth/profile` - Perfil del usuario
- `GET /auth/profile/edit` - Editar perfil
- `POST /auth/profile/edit` - Guardar cambios del perfil
- `GET /auth/change_password` - Cambiar contraseña
- `POST /auth/change_password` - Procesar cambio de contraseña
- `GET /auth/logout` - Cerrar sesión

### Rutas de Administración (Solo para admins)
- `GET /auth/admin/users` - Lista de usuarios
- `GET /auth/admin/user/<id>/toggle` - Activar/desactivar usuario

## 🎨 Interfaz de Usuario

### Características del Diseño

- **Diseño responsivo** que funciona en móviles y desktop
- **Gradientes modernos** con colores atractivos
- **Animaciones suaves** y efectos hover
- **Validación en tiempo real** de formularios
- **Mensajes flash** para feedback al usuario
- **Iconos Font Awesome** para mejor UX

### Componentes Principales

1. **Formularios de Autenticación**
   - Campos con floating labels
   - Validación visual en tiempo real
   - Indicador de fortaleza de contraseña
   - Mensajes de error contextuales

2. **Perfil de Usuario**
   - Información personal detallada
   - Estadísticas de uso
   - Acciones rápidas (editar, cambiar contraseña)
   - Badges de estado y rol

3. **Panel de Administración**
   - Tabla de usuarios con búsqueda
   - Estadísticas de usuarios
   - Acciones de gestión (activar/desactivar)
   - Filtros y ordenamiento

## 🔧 Configuración Avanzada

### Personalizar Validaciones

Editar las funciones en `auth.py`:

```python
def validar_password(password):
    """Personalizar requisitos de contraseña"""
    if len(password) < 8:  # Cambiar a 8 caracteres
        return False, "La contraseña debe tener al menos 8 caracteres"
    # Agregar más validaciones...
    return True, ""
```

### Configurar Roles Personalizados

Modificar el modelo `Usuario` en `models.py`:

```python
class Usuario(UserMixin, db.Model):
    # Agregar nuevos campos de rol
    es_profesor = db.Column(db.Boolean, default=False)
    es_estudiante = db.Column(db.Boolean, default=True)
```

### Personalizar Mensajes

Los mensajes flash se pueden personalizar en `auth.py`:

```python
flash('Mensaje personalizado', 'success')
```

## 🚨 Consideraciones de Seguridad

### En Producción

1. **Cambiar la SECRET_KEY** por una clave segura y única
2. **Habilitar HTTPS** y configurar `SESSION_COOKIE_SECURE = True`
3. **Configurar logging** para auditoría de seguridad
4. **Implementar rate limiting** para prevenir ataques de fuerza bruta
5. **Configurar backup** de la base de datos

### Recomendaciones

- Usar contraseñas fuertes (mínimo 8 caracteres)
- Cambiar la contraseña del admin por defecto
- Revisar logs regularmente
- Mantener las dependencias actualizadas

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de base de datos**
   ```bash
   # Eliminar y recrear la base de datos
   rm plataforma.db
   python app.py
   ```

2. **Error de importación**
   ```bash
   # Verificar instalación de dependencias
   pip install flask-login flask-sqlalchemy
   ```

3. **Problemas de sesión**
   - Verificar que SECRET_KEY esté configurada
   - Limpiar cookies del navegador

### Logs y Debugging

```python
# Habilitar debug en config.py
DEBUG = True
```

## 📈 Futuras Mejoras

- [ ] Recuperación de contraseña por email
- [ ] Autenticación de dos factores (2FA)
- [ ] Integración con redes sociales (OAuth)
- [ ] Sistema de permisos granular
- [ ] Auditoría de acciones de usuario
- [ ] API REST para autenticación
- [ ] Notificaciones por email
- [ ] Dashboard de administración avanzado

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades:

1. Revisar la documentación existente
2. Verificar los logs de la aplicación
3. Probar en un entorno limpio
4. Documentar los pasos para reproducir el problema

---

**Versión:** 2.0.0  
**Fecha:** 2025  
**Autor:** Plataforma Preuniversitaria 
# Sistema de Administración - Plataforma Preuniversitaria

## 👑 Panel de Administración

### Acceso al Panel
- **Ruta**: `/auth/admin/users`
- **Permisos**: Solo usuarios con `es_admin = True`
- **Acceso**: Desde el perfil del usuario (botón "Panel de Administración")

### Estadísticas del Sistema
El panel muestra estadísticas en tiempo real:
- **Total de Usuarios**: Número total de cuentas registradas
- **Usuarios Activos**: Cuentas con `es_activo = True`
- **Usuarios Premium**: Cuentas con premium activo
- **Administradores**: Usuarios con `es_admin = True`
- **Usuarios Google**: Cuentas registradas vía Google OAuth

## 🔧 Funcionalidades de Administración

### 1. Gestión de Usuarios

#### Activar/Desactivar Usuarios
- **Acción**: Botón de toggle en cada fila de usuario
- **Efecto**: Cambia el estado `es_activo` del usuario
- **Restricción**: No se puede desactivar tu propia cuenta

#### Convertir en Administrador
- **Acción**: Botón corona (👑) en cada fila
- **Efecto**: Cambia el estado `es_admin` del usuario
- **Restricción**: No se puede cambiar tu propio estado de admin

#### Eliminar Usuarios
- **Acción**: Botón de papelera (🗑️) en cada fila
- **Efecto**: Elimina completamente la cuenta y sus sesiones
- **Restricción**: No se pueden eliminar administradores ni tu propia cuenta

### 2. Sistema Premium

#### Otorgar Premium
- **Tipos disponibles**:
  - **Mensual**: 30 días de duración
  - **Anual**: 365 días de duración
  - **Permanente**: Sin fecha de expiración
- **Campos requeridos**:
  - Tipo de premium
  - Duración (días) - excepto para permanente
  - Razón del otorgamiento

#### Revocar Premium
- **Acción**: Cambiar a "Revocar Premium" en el modal
- **Efecto**: Desactiva premium y limpia fechas
- **Campo requerido**: Razón de la revocación

#### Verificación Automática
- El sistema verifica automáticamente la expiración de premium
- Los usuarios con premium expirado se marcan como no premium automáticamente

### 3. Acciones Masivas

#### Selección Múltiple
- **Checkbox individual**: Seleccionar usuarios específicos
- **Checkbox "Seleccionar Todo"**: Seleccionar todos los usuarios disponibles
- **Restricción**: Los administradores no se pueden seleccionar para eliminación

#### Acciones Disponibles
- **Activar Seleccionados**: Activar múltiples usuarios
- **Desactivar Seleccionados**: Desactivar múltiples usuarios
- **Eliminar Seleccionados**: Eliminar múltiples usuarios (solo no-admin)

### 4. Búsqueda y Filtrado

#### Búsqueda en Tiempo Real
- **Campos buscables**: Nombre, email, institución educativa
- **Funcionamiento**: Filtrado instantáneo sin recargar página
- **Búsqueda**: No sensible a mayúsculas/minúsculas

## 🎨 Interfaz de Usuario

### Diseño Responsivo
- **Mobile-friendly**: Adaptado para dispositivos móviles
- **Grid system**: Estadísticas en grid responsive
- **Tabla scrolleable**: Para manejar muchos usuarios

### Indicadores Visuales
- **Badges de estado**: Activo, Inactivo, Admin, Premium, Google
- **Colores distintivos**: Cada tipo de badge tiene su color
- **Iconos intuitivos**: FontAwesome para mejor UX

### Feedback Visual
- **Alertas**: Mensajes de éxito/error con auto-dismiss
- **Confirmaciones**: Diálogos de confirmación para acciones críticas
- **Loading states**: Indicadores durante operaciones AJAX

## 🔐 Seguridad y Permisos

### Validaciones de Seguridad
- **Verificación de permisos**: Todas las rutas verifican `es_admin`
- **Protección de auto-eliminación**: No se puede eliminar tu propia cuenta
- **Protección de administradores**: No se pueden eliminar otros admins
- **Validación de datos**: Todos los inputs se validan en backend

### Logs y Auditoría
- **Razones obligatorias**: Todas las acciones premium requieren razón
- **Timestamps**: Todas las acciones se registran con fecha/hora
- **Trazabilidad**: Se puede rastrear quién hizo qué y cuándo

## 📊 Modelo de Datos

### Campos Premium en Usuario
```python
es_premium = db.Column(db.Boolean, default=False)
fecha_premium_inicio = db.Column(db.DateTime, nullable=True)
fecha_premium_fin = db.Column(db.DateTime, nullable=True)
tipo_premium = db.Column(db.String(20), nullable=True)
razon_premium = db.Column(db.String(100), nullable=True)
```

### Métodos del Modelo
```python
def is_premium_active(self):
    """Verifica si el usuario tiene premium activo"""

def grant_premium(self, tipo, duracion_dias, razon):
    """Otorga premium al usuario"""

def revoke_premium(self, razon):
    """Revoca premium al usuario"""
```

## 🚀 Endpoints API

### Gestión de Usuarios
- `GET /auth/admin/users` - Panel principal
- `GET /auth/admin/toggle_user/<id>` - Activar/desactivar usuario
- `GET /auth/admin/toggle_admin/<id>` - Cambiar estado admin
- `POST /auth/admin/delete_user/<id>` - Eliminar usuario

### Gestión Premium
- `POST /auth/admin/grant_premium/<id>` - Otorgar premium
- `POST /auth/admin/revoke_premium/<id>` - Revocar premium

### Acciones Masivas
- `POST /auth/admin/bulk_actions` - Acciones en múltiples usuarios

## 📋 Casos de Uso

### Escenario 1: Otorgar Premium a un Estudiante Destacado
1. Ir al Panel de Administración
2. Buscar el usuario por nombre o email
3. Hacer clic en el botón estrella (⭐)
4. Seleccionar "Otorgar Premium"
5. Elegir tipo (ej: "Mensual")
6. Establecer duración (ej: 30 días)
7. Escribir razón (ej: "Estudiante destacado - Becado")
8. Guardar

### Escenario 2: Limpiar Cuentas Inactivas
1. Ir al Panel de Administración
2. Buscar usuarios inactivos
3. Seleccionar múltiples usuarios con checkboxes
4. Hacer clic en "Eliminar Seleccionados"
5. Confirmar la acción

### Escenario 3: Promover un Usuario a Administrador
1. Ir al Panel de Administración
2. Buscar el usuario
3. Hacer clic en el botón corona (👑)
4. Confirmar la acción
5. El usuario ahora tendrá acceso al panel de administración

## ⚠️ Consideraciones Importantes

### Limitaciones de Seguridad
- Los administradores no pueden eliminar otros administradores
- No se puede cambiar tu propio estado de administrador
- No se puede eliminar tu propia cuenta

### Gestión de Premium
- El premium se verifica automáticamente en cada acceso
- Los usuarios con premium expirado se marcan como no premium
- El premium permanente no tiene fecha de expiración

### Rendimiento
- La búsqueda se realiza en el frontend para mejor rendimiento
- Las acciones masivas se procesan en lotes
- Los cambios se reflejan inmediatamente sin recargar

## 🔄 Mantenimiento

### Tareas Programadas Recomendadas
- **Verificación diaria de premium**: Verificar expiración de premium
- **Limpieza de sesiones**: Eliminar sesiones antiguas
- **Backup de usuarios**: Respaldo regular de datos de usuarios

### Monitoreo
- **Logs de administración**: Registrar todas las acciones de admin
- **Métricas de uso**: Seguimiento de usuarios premium vs normales
- **Alertas**: Notificaciones para acciones críticas 
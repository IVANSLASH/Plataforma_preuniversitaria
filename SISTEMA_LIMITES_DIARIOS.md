# Sistema de Límites Diarios - Plataforma Preuniversitaria

## 📋 Resumen

Se ha implementado un sistema completo de restricción de visualización de ejercicios con límites diarios y suscripción premium. El sistema permite:

- **5 ejercicios diarios** para usuarios sin registro
- **15 ejercicios diarios** para usuarios registrados
- **Acceso ilimitado** para usuarios premium
- **Seguimiento automático** de ejercicios vistos por día
- **Página de suscripción premium** con diferentes planes

## 🏗️ Arquitectura del Sistema

### 1. Modelo de Usuario (`models.py`)

#### Nuevos Campos Agregados:
```python
# Campos para sistema de límites diarios
ejercicios_vistos_hoy = db.Column(db.Integer, default=0)  # Contador de ejercicios vistos hoy
ultima_fecha_conteo = db.Column(db.Date, nullable=True)  # Última fecha en que se contaron ejercicios
ejercicios_vistos_ids = db.Column(db.Text, nullable=True)  # IDs de ejercicios vistos hoy (JSON)
```

#### Nuevos Métodos:
- `reset_daily_count()`: Reinicia el contador diario
- `can_view_exercise(ejercicio_id)`: Verifica si puede ver un ejercicio
- `mark_exercise_as_viewed(ejercicio_id)`: Marca un ejercicio como visto
- `get_daily_limit_info()`: Obtiene información de límites diarios

### 2. Modelo de Seguimiento (`models.py`)

```python
class EjercicioVisto(db.Model):
    """Modelo para registrar ejercicios vistos por usuarios"""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    ejercicio_id = db.Column(db.String(50), nullable=False)
    fecha_visto = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    session_id = db.Column(db.String(100), nullable=True)
```

## 🔄 Flujo de Funcionamiento

### Para Usuarios Registrados:
1. **Verificación**: Al acceder a un ejercicio, se verifica `can_view_exercise()`
2. **Conteo**: Si puede ver, se marca con `mark_exercise_as_viewed()`
3. **Límite**: Se aplica límite de 15 ejercicios diarios
4. **Reinicio**: El contador se reinicia automáticamente cada día

### Para Usuarios Sin Registro:
1. **Sesión**: Se usa la sesión de Flask para tracking
2. **Límite**: Se aplica límite de 5 ejercicios diarios
3. **Persistencia**: Los datos se mantienen durante la sesión

### Para Usuarios Premium:
1. **Acceso Libre**: No se aplican restricciones
2. **Verificación**: Se verifica `is_premium_active()`
3. **Sin Conteo**: No se cuenta ejercicios vistos

## 🎯 Funcionalidades Implementadas

### 1. Página Principal (`/`)
- **Información de límites**: Muestra ejercicios vistos y restantes
- **Alertas**: Notifica cuando se alcanza el límite
- **Enlaces**: Botones para registrarse o ir premium
- **Filtrado**: Solo muestra ejercicios que el usuario puede ver

### 2. Detalle de Ejercicio (`/ejercicio/<id>`)
- **Verificación de acceso**: Bloquea si no puede ver
- **Página de bloqueo**: Muestra opciones para registrarse o premium
- **Conteo automático**: Marca como visto al acceder

### 3. Página Premium (`/premium`)
- **Planes disponibles**: Mensual, Anual, Permanente
- **Beneficios**: Lista de características premium
- **Comparación**: Tabla comparativa de planes
- **Formulario**: Solicitud de suscripción

### 4. Navegación
- **Enlace Premium**: Agregado al menú principal
- **Indicadores**: Badges y alertas de estado

## 🎨 Interfaz de Usuario

### Alertas de Límite Diario:
```html
<div class="alert alert-info">
    <strong>Límite diario:</strong> 
    Has visto X de Y ejercicios disponibles hoy.
    <span class="badge bg-success">Z restantes</span>
</div>
```

### Página de Bloqueo:
```html
<div class="card border-warning">
    <div class="card-header bg-warning">
        <h3><i class="fas fa-lock"></i> Acceso Restringido</h3>
    </div>
    <div class="card-body text-center">
        <!-- Opciones de registro y premium -->
    </div>
</div>
```

### Filtro de Materias Favoritas:
```css
.materias-favoritas-filter {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    /* Efectos hover y animaciones */
}
```

## 🔧 Herramientas de Administración

### Script de Gestión Premium (`otorgar_premium.py`):
```python
# Otorgar premium a un usuario
otorgar_premium_usuario("usuario@ejemplo.com", "mensual", 30)

# Listar usuarios premium
listar_usuarios_premium()

# Mostrar estadísticas
mostrar_estadisticas_limites()
```

### Métodos de Usuario:
```python
# Otorgar premium
usuario.grant_premium(tipo='mensual', duracion_dias=30)

# Revocar premium
usuario.revoke_premium(razon='Revocado por administrador')

# Verificar estado premium
usuario.is_premium_active()
```

## 📊 Límites y Configuración

### Límites por Tipo de Usuario:
- **Sin registro**: 5 ejercicios/día
- **Registrado**: 15 ejercicios/día
- **Premium**: Ilimitado

### Planes Premium:
- **Mensual**: $9.99/mes
- **Anual**: $99.99/año (20% descuento)
- **Permanente**: $299.99 (único pago)

### Beneficios Premium:
- ✅ Ejercicios ilimitados
- ✅ Descargas PDF
- ✅ Estadísticas avanzadas
- ✅ Soporte prioritario
- ✅ Contenido exclusivo

## 🚀 Implementación Técnica

### Base de Datos:
```sql
-- Nuevas columnas en tabla usuarios
ALTER TABLE usuarios ADD COLUMN ejercicios_vistos_hoy INTEGER DEFAULT 0;
ALTER TABLE usuarios ADD COLUMN ultima_fecha_conteo DATE;
ALTER TABLE usuarios ADD COLUMN ejercicios_vistos_ids TEXT;

-- Nueva tabla para seguimiento
CREATE TABLE ejercicios_vistos (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER,
    ejercicio_id VARCHAR(50) NOT NULL,
    fecha_visto DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(100)
);
```

### Rutas Implementadas:
- `GET /`: Página principal con límites
- `GET /ejercicio/<id>`: Detalle con verificación
- `GET /premium`: Página de suscripción
- `POST /api/ejercicios`: API con filtrado

### Variables de Plantilla:
```python
limites_info = {
    'limite_diario': 15,  # o 5 para sin registro
    'ejercicios_vistos': 3,
    'ejercicios_restantes': 12,
    'es_premium': False,
    'tipo_usuario': 'registrado'  # o 'sin_registro'
}
```

## 🔒 Seguridad y Validación

### Validaciones Implementadas:
1. **Verificación de fecha**: Reinicio automático diario
2. **Conteo de ejercicios**: Prevención de duplicados
3. **Estado premium**: Verificación de vigencia
4. **Sesión segura**: Tracking para usuarios sin registro

### Protecciones:
- **SQL Injection**: Uso de ORM SQLAlchemy
- **XSS**: Escape automático en templates
- **CSRF**: Protección en formularios
- **Rate Limiting**: Conteo por sesión/usuario

## 📈 Métricas y Análisis

### Datos Recopilados:
- Ejercicios vistos por usuario
- Fechas de visualización
- IP addresses (para auditoría)
- User agents
- Patrones de uso

### Estadísticas Disponibles:
- Usuarios activos por día
- Ejercicios más populares
- Conversión a premium
- Retención de usuarios

## 🎯 Próximos Pasos

### Mejoras Futuras:
1. **Notificaciones**: Alertas cuando se acerca al límite
2. **Analytics**: Dashboard de uso detallado
3. **Gamificación**: Logros por ejercicios completados
4. **Recomendaciones**: Ejercicios sugeridos
5. **Social**: Compartir progreso
6. **Mobile**: App nativa

### Optimizaciones:
1. **Caché**: Redis para contadores
2. **CDN**: Imágenes y recursos estáticos
3. **Compresión**: Gzip para respuestas
4. **Lazy Loading**: Carga progresiva de ejercicios

## 📝 Notas de Implementación

### Consideraciones:
- El sistema es compatible con usuarios existentes
- Los límites se aplican de forma transparente
- La migración de base de datos es automática
- El sistema es escalable y mantenible

### Dependencias:
- Flask-SQLAlchemy para ORM
- Flask-Login para autenticación
- Bootstrap para UI
- Font Awesome para iconos

---

**Autor**: Plataforma Preuniversitaria  
**Fecha**: 2025  
**Versión**: 1.0 
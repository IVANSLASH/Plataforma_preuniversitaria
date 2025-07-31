# Sistema de Límites Diarios y Suscripción Premium

## Resumen

Este documento describe el sistema implementado para limitar el acceso a ejercicios y simulacros, y ofrecer una suscripción premium en la Plataforma Preuniversitaria.

### Funcionalidades Implementadas

1. **Límites diarios de ejercicios:**
   - Usuarios sin registro: 5 ejercicios por día
   - Usuarios registrados: 15 ejercicios por día
   - Usuarios premium: Sin límites

2. **Límites diarios de simulacros:**
   - Usuarios sin registro: 0 simulacros por día
   - Usuarios registrados: 1 simulacro por día
   - Usuarios premium: Simulacros ilimitados

3. **Sistema de suscripción premium:**
   - Planes mensual, anual y permanente
   - Beneficios ilimitados para ejercicios y simulacros
   - Página dedicada de información y solicitud

4. **Interfaz de usuario:**
   - Indicadores de límites en la página principal
   - Mensajes de restricción en detalle de ejercicios
   - Información de límites en página de simulacros
   - Navegación hacia registro y premium

## Arquitectura del Sistema

### Nuevos Campos en el Modelo Usuario

```python
# Campos para sistema de límites diarios
ejercicios_vistos_hoy = db.Column(db.Integer, default=0)
ultima_fecha_conteo = db.Column(db.Date, nullable=True)
ejercicios_vistos_ids = db.Column(db.Text, nullable=True)  # JSON de IDs

# Campos para sistema de límites de simulacros
simulacros_realizados_hoy = db.Column(db.Integer, default=0)
ultima_fecha_simulacro = db.Column(db.Date, nullable=True)

# Campos para sistema premium
es_premium = db.Column(db.Boolean, default=False)
fecha_premium_inicio = db.Column(db.DateTime, nullable=True)
fecha_premium_fin = db.Column(db.DateTime, nullable=True)
tipo_premium = db.Column(db.String(20), nullable=True)
razon_premium = db.Column(db.String(100), nullable=True)
```

### Nuevos Métodos en el Modelo Usuario

#### Para Ejercicios:
- `reset_daily_count()`: Reinicia contadores si es un nuevo día
- `can_view_exercise(ejercicio_id)`: Verifica si puede ver un ejercicio
- `mark_exercise_as_viewed(ejercicio_id)`: Marca ejercicio como visto
- `get_daily_limit_info()`: Obtiene información de límites

#### Para Simulacros:
- `reset_simulacro_count()`: Reinicia contadores de simulacros
- `can_do_simulacro()`: Verifica si puede hacer simulacro
- `mark_simulacro_as_done()`: Marca simulacro como realizado
- `get_simulacro_limit_info()`: Obtiene información de límites de simulacros

## Flujo Operacional

### Para Usuarios Sin Registro

1. **Ejercicios:**
   - Límite: 5 ejercicios por día
   - Tracking: Usando Flask session
   - Variables: `ejercicios_vistos_hoy`, `ultima_fecha_conteo`, `ejercicios_vistos_ids`

2. **Simulacros:**
   - Límite: 0 simulacros por día
   - Acceso: Bloqueado completamente
   - Mensaje: "Debes registrarte para realizar simulacros"

### Para Usuarios Registrados

1. **Ejercicios:**
   - Límite: 15 ejercicios por día
   - Tracking: En base de datos
   - Reset: Automático cada día

2. **Simulacros:**
   - Límite: 1 simulacro por día
   - Tracking: En base de datos
   - Reset: Automático cada día

### Para Usuarios Premium

1. **Ejercicios:**
   - Límite: Ilimitado
   - Tracking: No aplica
   - Acceso: Completo

2. **Simulacros:**
   - Límite: Ilimitado
   - Tracking: No aplica
   - Acceso: Completo

## Funcionalidades Implementadas

### Página Principal (`/`)

- **Barra de límites diarios:** Reposicionada al final de la página con estilo menos prominente
- **Filtrado de ejercicios:** Muestra ejercicios disponibles vs bloqueados
- **Indicadores visuales:** Badges de "restantes" o "límite alcanzado"
- **Enlaces de acción:** Registro y premium

### Detalle de Ejercicio (`/ejercicio/<id>`)

- **Verificación de acceso:** Antes de mostrar contenido
- **Mensaje de restricción:** Si no puede ver el ejercicio
- **Información de límites:** Contexto sobre restricciones
- **Opciones de acción:** Registro y premium

### Página de Simulacros (`/simulacro`)

- **Información de límites:** Barra informativa sobre simulacros disponibles
- **Botón condicional:** Habilitado/deshabilitado según límites
- **Verificación en backend:** Antes de generar simulacro
- **Marcado automático:** Cuando se genera simulacro

### Página Premium (`/premium`)

- **Información detallada:** Beneficios y planes disponibles
- **Estado actual:** Límites del usuario
- **Formulario de solicitud:** Para contactar administradores
- **Comparación:** Free vs Premium

### Navegación

- **Link Premium:** En barra de navegación principal
- **Acceso condicional:** Solo para usuarios no premium

## Elementos de UI

### Barra de Límites Diarios (Página Principal)

```html
<!-- Información de límites diarios (al final de la página) -->
{% if not limites_info.es_premium %}
<div class="row mt-5">
    <div class="col-12">
        <div class="alert alert-light border" role="alert" style="opacity: 0.8; font-size: 0.9em;">
            <!-- Contenido de límites -->
        </div>
    </div>
</div>
{% endif %}
```

### Información de Simulacros

```html
<!-- Información de límites de simulacros -->
{% if not simulacro_info.es_premium %}
<div class="row mb-4">
    <div class="col-12">
        <div class="alert alert-info" role="alert">
            <!-- Contenido de límites de simulacros -->
        </div>
    </div>
</div>
{% endif %}
```

### Botón Condicional de Simulacro

```html
{% if simulacro_info.puede_hacer %}
<button type="submit" class="btn btn-danger btn-lg">
    <i class="fas fa-magic"></i> Generar Simulacro
</button>
{% else %}
<button type="submit" class="btn btn-secondary btn-lg" disabled>
    <i class="fas fa-ban"></i> Límite de Simulacros Alcanzado
</button>
{% endif %}
```

## Herramientas de Administración

### Script `otorgar_premium.py`

Comandos disponibles:

```bash
# Otorgar premium
python otorgar_premium.py otorgar usuario@ejemplo.com
python otorgar_premium.py otorgar usuario@ejemplo.com mensual 30 'Prueba'

# Listar usuarios premium
python otorgar_premium.py listar

# Ver estadísticas de límites
python otorgar_premium.py estadisticas

# Resetear límites de usuario
python otorgar_premium.py resetear usuario@ejemplo.com

# Ver límites de simulacros
python otorgar_premium.py simulacros
```

## Límites y Configuración

### Límites Actuales

| Tipo Usuario | Ejercicios/Día | Simulacros/Día |
|--------------|----------------|----------------|
| Sin registro | 5 | 0 |
| Registrado | 15 | 1 |
| Premium | Ilimitado | Ilimitado |

### Configuración

Los límites están definidos en:
- `models.py`: En los métodos `get_daily_limit_info()` y `get_simulacro_limit_info()`
- `app.py`: En las rutas que verifican límites

## Implementación Técnica

### Esquema de Base de Datos

```sql
-- Campos agregados a la tabla usuarios
ALTER TABLE usuarios ADD COLUMN ejercicios_vistos_hoy INTEGER DEFAULT 0;
ALTER TABLE usuarios ADD COLUMN ultima_fecha_conteo DATE;
ALTER TABLE usuarios ADD COLUMN ejercicios_vistos_ids TEXT;
ALTER TABLE usuarios ADD COLUMN simulacros_realizados_hoy INTEGER DEFAULT 0;
ALTER TABLE usuarios ADD COLUMN ultima_fecha_simulacro DATE;
```

### Rutas Modificadas

1. **`/` (index):**
   - Filtrado de ejercicios por límites
   - Información de límites en template

2. **`/ejercicio/<id>`:**
   - Verificación de acceso
   - Marcado de ejercicio como visto

3. **`/simulacro`:**
   - Información de límites de simulacros
   - Verificación antes de generar

4. **`/generar_simulacro` y `/generar_simulacro_pdf`:**
   - Verificación de límites
   - Marcado de simulacro como realizado

5. **`/premium` (nueva):**
   - Información de suscripción premium

### Variables de Template

#### Para Ejercicios:
```python
limites_info = {
    'limite_diario': 15,
    'ejercicios_vistos': 5,
    'ejercicios_restantes': 10,
    'es_premium': False,
    'tipo_usuario': 'registrado'
}
```

#### Para Simulacros:
```python
simulacro_info = {
    'limite_diario': 1,
    'simulacros_realizados': 0,
    'simulacros_restantes': 1,
    'es_premium': False,
    'puede_hacer': True
}
```

## Seguridad

### Verificaciones Implementadas

1. **Autenticación:** Verificación de `current_user.is_authenticated`
2. **Autorización:** Verificación de `current_user.es_admin` para funciones administrativas
3. **Límites:** Verificación en cada acceso a ejercicios y simulacros
4. **Session:** Para usuarios sin registro, usando Flask session

### Protección contra Bypass

- Verificación en backend antes de servir contenido
- Marcado automático de uso
- Reset diario automático
- Tracking de IDs de ejercicios vistos

## Métricas y Análisis

### Datos Recopilados

1. **Ejercicios vistos:** Por usuario y por día
2. **Simulacros realizados:** Por usuario y por día
3. **Estado premium:** Usuarios con suscripción activa
4. **Patrones de uso:** Frecuencia y distribución

### Modelo de Auditoría

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

## Mejoras Futuras

### Funcionalidades Sugeridas

1. **Dashboard de administración:**
   - Interfaz web para gestionar usuarios premium
   - Estadísticas en tiempo real
   - Gestión de límites por usuario

2. **Sistema de notificaciones:**
   - Alertas cuando se acerca al límite
   - Recordatorios de renovación premium
   - Notificaciones de nuevos beneficios

3. **Análisis avanzado:**
   - Reportes de uso por materia
   - Patrones de estudio
   - Recomendaciones personalizadas

4. **Flexibilidad de límites:**
   - Límites configurables por administrador
   - Bonificaciones por actividad
   - Límites especiales para eventos

### Optimizaciones Técnicas

1. **Cache de límites:**
   - Reducir consultas a base de datos
   - Cache en Redis para alta concurrencia

2. **Batch processing:**
   - Reset diario automático programado
   - Limpieza de datos antiguos

3. **API endpoints:**
   - Endpoints para verificar límites
   - Integración con aplicaciones móviles

## Conclusión

El sistema de límites diarios y suscripción premium proporciona una base sólida para monetizar la plataforma mientras mantiene el acceso gratuito limitado. La implementación es robusta, escalable y proporciona una experiencia de usuario clara sobre las restricciones y beneficios disponibles. 
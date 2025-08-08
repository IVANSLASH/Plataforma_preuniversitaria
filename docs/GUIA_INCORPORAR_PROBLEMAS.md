# 👨‍💼 GUÍA ADMINISTRATIVA: Gestión de la Plataforma Preuniversitaria

## 🎯 **OBJETIVO**
Esta guía está dirigida a administradores que necesitan gestionar usuarios, contenido y funcionalidades de la plataforma web Flask.

---

## 👨‍💼 **ACCESO ADMINISTRATIVO**

### 1.1 Convertirse en administrador
```bash
# Opción 1: Email hardcodeado (automático)
# El email "ingivanladislao@gmail.com" es automáticamente administrador

# Opción 2: Script de administrador
python hacer_admin.py
```

### 1.2 Acceder al panel de administración
1. **Iniciar sesión** con Google OAuth como administrador
2. **Ir a**: http://localhost:5000/admin/users
3. **Panel disponible** automáticamente para administradores

### 1.3 Verificar permisos administrativos
- ✅ Acceso a `/admin/users`
- ✅ Acceso a `/estadisticas` 
- ✅ Funciones de gestión de usuarios
- ✅ Otorgamiento de premium

---

## 👥 **GESTIÓN DE USUARIOS**

### 2.1 Panel de administración de usuarios
**Ubicación:** `/admin/users`

**Funcionalidades disponibles:**
- 📋 **Listar todos los usuarios** registrados
- 🔍 **Buscar usuarios** por email o nombre
- 👑 **Otorgar privilegios** de administrador
- 💎 **Gestionar cuentas premium**
- 📊 **Ver estadísticas** de uso por usuario
- 🚫 **Desactivar/activar** cuentas

### 2.2 Gestión de cuentas premium
```bash
# Script de gestión premium
python otorgar_premium.py

# Funciones disponibles:
# - Otorgar premium mensual/anual/permanente
# - Revocar premium
# - Listar usuarios premium
# - Ver estadísticas
```

### 2.3 Tipos de usuarios en la plataforma:

| Tipo | Límite Diario | Descripción | Gestión |
|------|---------------|-------------|---------|
| **Sin registro** | 5 ejercicios | Usuarios anónimos | Automático por sesión |
| **Registrado** | 15 ejercicios | Google OAuth | Panel admin |
| **Premium** | Ilimitado | Suscripción pagada | Script/Panel admin |
| **Administrador** | Ilimitado | Gestión completa | Script `hacer_admin.py` |

**Estados premium:**
- `mensual` - Duración: 30 días
- `anual` - Duración: 365 días  
- `permanente` - Sin expiración
- `revocado` - Premium revocado

---

## 📊 **ESTADÍSTICAS Y MONITOREO**

### 3.1 Página de estadísticas
**Ubicación:** `/estadisticas` (Solo administradores)

**Métricas disponibles:**
- 👥 **Usuarios registrados** total y por período
- 📈 **Ejercicios vistos** por día/semana/mes
- 💎 **Conversiones a premium** y ingresos estimados
- 🎯 **Ejercicios más populares** y menos accedidos
- 📱 **Patrones de uso** por dispositivo/hora
- 🔄 **Retención de usuarios** y sesiones activas

### 3.2 Datos de seguimiento automático
```python
# La aplicación registra automáticamente:
# - Ejercicios vistos por usuario/sesión
# - Fechas y horarios de acceso
# - IPs y user agents (para análisis)
# - Límites diarios alcanzados
# - Conversiones a premium
```

### 3.3 Scripts de utilidad administrativa

**Archivo:** `hacer_admin.py`
```python
# Convertir usuario en administrador
# Uso: python hacer_admin.py
# Permite seleccionar usuario por email
# Otorga privilegios administrativos
```

**Archivo:** `otorgar_premium.py`
```python
# Gestión completa de cuentas premium
# Funciones:
# - otorgar_premium_usuario(email, tipo, dias)
# - revocar_premium_usuario(email, razon)
# - listar_usuarios_premium()
# - mostrar_estadisticas_limites()
```

### 3.4 Base de datos y modelos

**Modelos principales:**
```python
# Usuario - Información básica y premium
class Usuario(UserMixin, db.Model):
    # Campos: email, nombre, es_admin, es_premium
    # Métodos: grant_premium(), is_premium_active()
    
# EjercicioVisto - Tracking de ejercicios
class EjercicioVisto(db.Model):
    # Registro de ejercicios vistos por usuario
    # Campos: usuario_id, ejercicio_id, fecha_visto
    
# SesionUsuario - Límites para no registrados
class SesionUsuario(db.Model):
    # Control de límites por sesión
    # Campos: session_id, ejercicios_vistos_hoy
```

---

## 🛠️ **GESTIÓN DE CONTENIDO**

### 4.1 Estructura actual de ejercicios
```
ejercicios_nuevo/
├── matematicas_preuniversitaria/
│   ├── algebra/     (6 ejercicios: MATU_ALG_001-006)
│   ├── funciones/   (2 ejercicios: MATU_FUN_007-008)  
│   └── geometria/   (2 ejercicios: MATU_GEO_010-011)
└── fisica_preuniversitaria/
    └── dinamica/    (2 ejercicios: FISU_DIN_001, FISU_CIN_009)
```

### 4.2 Exportar/actualizar ejercicios
```bash
# Script para exportar ejercicios a JSON
python exportador/exportar_json_nuevo.py

# Archivos generados:
# - etiquetas/metadata_ejercicios_nuevo.json
# - etiquetas/todos_ejercicios_nuevo.json
# - etiquetas/matematicas_preuniversitaria_nuevo.json
# - etiquetas/fisica_preuniversitaria_nuevo.json
```

---

## 🌐 **FUNCIONALIDADES WEB ADMINISTRATIVAS**

### 5.1 Rutas administrativas
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/admin/users` | Panel de usuarios | Solo administradores |
| `/estadisticas` | Métricas del sistema | Solo administradores |
| `/premium` | Gestión de suscripciones | Todos los usuarios |

### 5.2 Funcionalidades del panel de usuarios
- **Buscar usuarios:** Por email, nombre o estado
- **Modificar roles:** Otorgar/revocar administrador
- **Gestionar premium:** Otorgar/revocar suscripciones
- **Ver actividad:** Ejercicios vistos, última actividad
- **Estadísticas:** Métricas de uso por usuario

---

## 📄 **GENERACIÓN DE CONTENIDO PDF**

### 6.1 Simulacros personalizados
Los usuarios pueden generar simulacros desde la interfaz web:
- **Filtros disponibles:** Materia, capítulo, nivel, número de preguntas
- **Formatos:** PDF descargable con ReportLab
- **Personalización:** Título, instrucciones, tiempo

### 6.2 Gestión de libros LaTeX (Legado)
```bash
# Los libros en libros/ son de la estructura antigua
# Para uso actual, los ejercicios se muestran directamente en web
# con MathJax para renderizado matemático
```

---

## 🎓 **GESTIÓN DE SIMULACROS**

### 7.1 Funcionalidad web de simulacros
**Ubicación:** `/simulacro`
- **Interfaz web:** Los usuarios crean simulacros desde la aplicación
- **Filtros dinámicos:** Por materia, capítulo disponible
- **Validaciones:** Número de preguntas disponibles
- **Generación PDF:** Automática con ReportLab

### 7.2 Control administrativo
- **Límites por usuario:** Sin registro (limitado), Premium (ilimitado)
- **Tracking:** Se registra cada simulacro generado
- **Estadísticas:** Simulacros más populares, materias preferidas

---

## ⚠️ **BUENAS PRÁCTICAS ADMINISTRATIVAS**

### ✅ **HACER:**
- **Monitorear límites diarios:** Verificar que el sistema funciona correctamente
- **Gestionar premium responsablemente:** Otorgar solo cuando corresponda
- **Revisar estadísticas regularmente:** Para identificar tendencias
- **Mantener backups:** De la base de datos SQLite
- **Documentar cambios:** Al modificar configuraciones

### ❌ **NO HACER:**
- **Otorgar admin indiscriminadamente:** Mantener control de acceso
- **Modificar base de datos directamente:** Usar scripts proporcionados
- **Ignorar métricas de error:** Revisar logs regularmente
- **Cambiar configuraciones sin respaldo:** Mantener archivo .env seguro

---

## 🔧 **SOLUCIÓN DE PROBLEMAS ADMINISTRATIVOS**

### Problema: "Usuario no puede acceder al panel admin"
**Solución:** Verificar que sea administrador con `hacer_admin.py`

### Problema: "Límites diarios no funcionan"
**Solución:** Revisar modelo `EjercicioVisto` y lógica de conteo

### Problema: "Error en Google OAuth"
**Solución:** Verificar credenciales en `.env` y configuración Google Console

### Problema: "Premium no se otorga"
**Solución:** Usar script `otorgar_premium.py` y verificar base de datos

---

## 📋 **CÓDIGOS DE MATERIAS ACTUALES**

### **Estructura de IDs implementada:**
| Materia Completa | Código | Ejemplo |
|------------------|--------|----------|
| Matemáticas Preuniversitaria | `MATU` | `MATU_ALG_001` |
| Física Preuniversitaria | `FISU` | `FISU_DIN_001` |

### **Capítulos disponibles:**
- **MATU_ALG**: Álgebra (6 ejercicios)
- **MATU_FUN**: Funciones (2 ejercicios)
- **MATU_GEO**: Geometría (2 ejercicios)  
- **FISU_DIN**: Dinámica (1 ejercicio)
- **FISU_CIN**: Cinemática (1 ejercicio)

**Más códigos disponibles en:** `docs/CODIGOS_MATERIAS.md`

---

## 🎯 **CHECKLIST ADMINISTRATIVO**

### **Gestión diaria:**
- [ ] Revisar estadísticas de uso
- [ ] Verificar funcionamiento de límites diarios
- [ ] Monitorear conversiones a premium
- [ ] Revisar logs de errores
- [ ] Verificar autenticación Google OAuth

### **Gestión de usuarios:**
- [ ] Revisar nuevos registros
- [ ] Gestionar solicitudes premium
- [ ] Atender reportes de problemas
- [ ] Mantener base de datos organizada

---

## 🚀 **PRÓXIMOS PASOS COMO ADMINISTRADOR**

1. **Familiarizarse** con el panel administrativo
2. **Configurar monitoreo** de métricas clave
3. **Establecer procesos** de gestión de usuarios
4. **Documentar procedimientos** específicos
5. **Planificar expansión** de contenido

---

**¿Necesitas ayuda administrativa?** 
- 📧 Revisar logs en `/var/log/` o consola
- 📖 Consultar `SISTEMA_LIMITES_DIARIOS.md`
- 🛠️ Usar scripts en la raíz del proyecto
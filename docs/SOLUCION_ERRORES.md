# 🔧 Soluciones para Problemas Comunes - Plataforma Preuniversitaria

## 📋 **Errores Comunes de la Aplicación Web**

### 1. **Error de Autenticación OAuth**
```
Error: invalid_client - The OAuth client was not found
```

**Causa:** Configuración incorrecta de Google OAuth.

**Solución:**
```bash
# 1. Verificar variables en .env
GOOGLE_CLIENT_ID=tu_client_id_real.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_real

# 2. Verificar URIs autorizadas en Google Cloud Console:
# - http://localhost:5000/auth/authorize
# - https://tu-dominio.com/auth/authorize (para producción)

# 3. Verificar que las APIs estén habilitadas:
# - Google+ API
# - Gmail API (opcional)
```

### 2. **Error 404 - Página no encontrada**
```
127.0.0.1 - - [08/Aug/2025 12:30:45] "GET /ejercicio/INVALID_ID HTTP/1.1" 404 -
```

**Causa:** ID de ejercicio no existe en la base de datos o estructura JSON.

**Solución:**
```bash
# 1. Verificar ejercicios disponibles
python exportador/exportar_json_nuevo.py

# 2. Revisar archivos JSON en etiquetas/
ls etiquetas/

# 3. Verificar estructura de ejercicios
ls ejercicios_nuevo/
```

### 3. **Error de Base de Datos**
```
OperationalError: no such table: usuarios
```

**Causa:** Base de datos no inicializada.

**Solución:**
```python
# La base de datos se inicializa automáticamente al ejecutar:
python app.py

# Si persiste el error, eliminar y recrear:
rm instance/plataforma.db
python app.py
```

---

## 🛠️ **Soluciones Implementadas Actuales**

### **Solución 1: Sistema de Límites Diarios**

**Funcionalidad:** Control automático de ejercicios por usuario/sesión.

**Implementación:**
```python
# En models.py
def can_view_exercise(self, ejercicio_id):
    """Verifica si el usuario puede ver un ejercicio"""
    if self.is_premium_active():
        return True
    # Lógica de límites para usuarios normales

def mark_exercise_as_viewed(self, ejercicio_id):
    """Marca un ejercicio como visto"""
    # Registro en EjercicioVisto
```

**Resultado:**
- ✅ Usuarios sin registro: 5 ejercicios/día
- ✅ Usuarios registrados: 15 ejercicios/día  
- ✅ Usuarios premium: ilimitado
- ✅ Reinicio automático diario

### **Solución 2: Manejo de Errores de Simulacros**

**Problema anterior:** Errores 400 en generación de simulacros.

**Solución implementada:**
```python
# En app.py - ruta /generar_simulacro
def generar_simulacro():
    # Validaciones mejoradas:
    # - Número de preguntas válido [5, 7, 8, 10, 12, 15, 20]
    # - Suficientes ejercicios disponibles
    # - Materia válida
    
    if num_preguntas not in [5, 7, 8, 10, 12, 15, 20]:
        return jsonify({'error': 'Número de preguntas no válido'}), 400
```

**Resultado:**
- ✅ Validación robusta de parámetros
- ✅ Mensajes de error informativos
- ✅ Generación exitosa de PDFs con ReportLab

### **Solución 3: Autenticación Google OAuth**

**Implementación completa:**
```python
# En auth.py
@auth_bp.route('/authorize')
def authorize():
    # Manejo completo del flujo OAuth
    # - Verificación de estado
    # - Obtención de tokens
    # - Creación/actualización de usuarios
```

**Resultado:**
- ✅ Registro automático con Google
- ✅ Manejo de perfiles existentes
- ✅ Asignación automática de roles admin

---

## 📁 **Estructura de Archivos Corregida**

### **Estructura Actual (Correcta):**
```
plataforma-preuniversitaria/
├── app.py                    # Aplicación Flask principal
├── auth.py                   # Sistema OAuth
├── models.py                 # Modelos de BD
├── config.py                 # Configuraciones

├── ejercicios_nuevo/         # Ejercicios activos
│   ├── matematicas_preuniversitaria/
│   │   ├── algebra/         (MATU_ALG_001-006)
│   │   ├── funciones/       (MATU_FUN_007-008)
│   │   └── geometria/       (MATU_GEO_010-011)
│   └── fisica_preuniversitaria/
│       └── dinamica/        (FISU_DIN_001, FISU_CIN_009)

├── templates/               # Templates HTML
├── static/                  # Archivos estáticos
├── etiquetas/              # Metadatos JSON
└── instance/               # Base de datos SQLite
```

### **Archivos Eliminados (Obsoletos):**
```
# Estas estructuras fueron removidas por ser redundantes:
frontend/                   # ❌ Eliminado - HTML standalone
ejercicios/                # ❌ Eliminado - Estructura antigua
static/ejercicios/         # ❌ Eliminado - Duplicados
```

---

## 🧪 **Herramientas de Verificación**

### **Scripts de Administración:**
```bash
# Verificar usuarios
python hacer_admin.py

# Gestionar premium
python otorgar_premium.py

# Exportar ejercicios
python exportador/exportar_json_nuevo.py
```

### **Endpoints de Prueba:**
```bash
# Verificar aplicación
curl http://localhost:5000/

# Verificar autenticación (debe redirigir)
curl -I http://localhost:5000/auth/login

# Verificar ejercicio específico
curl http://localhost:5000/ejercicio/MATU_ALG_001
```

---

## 🎯 **Resultados Esperados Actuales**

### **Después de las configuraciones correctas:**

1. **Autenticación:**
   - ✅ Login con Google OAuth funcional
   - ✅ Registro automático de nuevos usuarios
   - ✅ Asignación correcta de roles

2. **Ejercicios:**
   - ✅ 12 ejercicios disponibles en total
   - ✅ Límites diarios funcionando
   - ✅ Navegación correcta entre ejercicios

3. **Simulacros:**
   - ✅ Generación exitosa con parámetros válidos
   - ✅ PDFs descargables correctos
   - ✅ Validación de límites por tipo de usuario

4. **Panel Administrativo:**
   - ✅ Acceso restringido a administradores
   - ✅ Gestión de usuarios funcional
   - ✅ Estadísticas precisas

---

## 🚀 **Procedimiento de Verificación Completa**

### **1. Verificar Configuración:**
```bash
# Verificar variables de entorno
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_CLIENT_SECRET

# Verificar estructura de archivos
ls ejercicios_nuevo/
ls etiquetas/
```

### **2. Iniciar Aplicación:**
```bash
# Activar entorno virtual
source plataforma_env/bin/activate  # Linux/macOS
# plataforma_env\Scripts\activate   # Windows

# Iniciar aplicación
python app.py
```

### **3. Probar Funcionalidades:**
- **Acceso principal:** http://localhost:5000
- **Login Google:** http://localhost:5000/auth/login  
- **Ejercicio específico:** http://localhost:5000/ejercicio/MATU_ALG_001
- **Simulacros:** http://localhost:5000/simulacro
- **Admin (si tienes permisos):** http://localhost:5000/admin/users

---

## 📊 **Métricas de Mejora**

| Funcionalidad | Estado Anterior | Estado Actual |
|---------------|----------------|---------------|
| **Autenticación** | ❌ Manual/básica | ✅ Google OAuth |
| **Límites diarios** | ❌ No existían | ✅ Sistema completo |
| **Base de datos** | ❌ Archivos JSON | ✅ SQLite + ORM |
| **UI/UX** | ❌ HTML básico | ✅ Bootstrap 5 responsive |
| **PDFs** | ❌ LaTeX manual | ✅ ReportLab automático |
| **Administración** | ❌ Sin panel | ✅ Panel completo |
| **Estadísticas** | ❌ No disponibles | ✅ Métricas detalladas |
| **Seguridad** | ❌ Básica | ✅ OAuth + validaciones |

---

## 🔍 **Verificación de Estado del Sistema**

### **Comandos de Diagnóstico:**
```bash
# Estado de la aplicación
ps aux | grep python

# Verificar logs
tail -f /var/log/syslog | grep python

# Estado de la base de datos
sqlite3 instance/plataforma.db ".tables"
sqlite3 instance/plataforma.db "SELECT COUNT(*) FROM usuarios;"

# Verificar archivos críticos
ls -la .env
ls -la instance/
ls -la etiquetas/
```

### **Indicadores de Salud:**
- ✅ **Puerto 5000 activo:** `netstat -tlnp | grep :5000`
- ✅ **Base de datos accesible:** Tablas usuarios, ejercicios_vistos, etc.
- ✅ **Archivos JSON actualizados:** Fechas recientes en etiquetas/
- ✅ **OAuth configurado:** Variables .env correctas

---

## 📝 **Notas de Mantenimiento**

### **Tareas Regulares:**
- **Backup de BD:** `cp instance/plataforma.db backups/`
- **Actualizar ejercicios:** `python exportador/exportar_json_nuevo.py`
- **Revisar logs:** Verificar errores en consola de Flask
- **Monitorear usuarios:** Panel `/admin/users` y `/estadisticas`

### **Actualizaciones del Sistema:**
- **Dependencias:** `pip install --upgrade -r requirements.txt`
- **Base de datos:** Migraciones automáticas con SQLAlchemy
- **Configuraciones:** Revisar y actualizar `.env` según necesidades

---

**¿Problemas no resueltos?** 
- 📧 Revisar logs detallados en la consola
- 📖 Consultar documentación en `docs/`
- 🛠️ Usar scripts de utilidad para diagnóstico